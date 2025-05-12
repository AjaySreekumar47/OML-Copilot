#!/usr/bin/env python3
"""
Demo script for OML Copilot
"""

import os
import argparse
import ollama

from src.rag.retriever import OMLRetriever
from src.rag.embeddings import EmbeddingManager
from src.rag.examples_processor import ExamplesProcessor
from src.validation.validator import OMLValidator
from src.validation.error_handler import ErrorHandler
from src.validation.feedback_loop import FeedbackLoop
from src.dependency.vocabulary_manager import VocabularyManager

def main():
    parser = argparse.ArgumentParser(description='OML Copilot Demo')
    parser.add_argument('--examples', '-e', type=str, default='src/rag/examples_db/examples.jsonl',
                        help='Examples database file')
    parser.add_argument('--workspace', '-w', type=str, default='examples',
                        help='Workspace directory with OML files')
    parser.add_argument('--grammar', '-g', type=str, default='src/grammar/oml3_lark.txt',
                        help='Grammar file')
    parser.add_argument('--model', '-m', type=str, default='mistral',
                        help='Ollama model name')
    args = parser.parse_args()
    
    print("Initializing OML Copilot...")
    
    # Set up embedding manager
    embedding_manager = EmbeddingManager()
    
    # Load examples
    examples_processor = ExamplesProcessor(embedding_manager)
    examples = examples_processor.load_examples(args.examples)
    
    # Process examples
    vector_db = examples_processor.process_examples(examples)
    
    # Create retriever
    retriever = OMLRetriever(vector_db, embedding_manager)
    
    # Set up validator
    validator = OMLValidator(args.grammar)
    
    # Set up error handler
    error_handler = ErrorHandler(retriever)
    
    # Set up vocabulary manager
    vocabulary_manager = VocabularyManager(args.workspace)
    
    # Set up feedback loop
    feedback_loop = FeedbackLoop(ollama, validator, error_handler)
    
    print("\nOML Copilot initialized.")
    print(f"Loaded {len(examples)} examples from {args.examples}")
    print(f"Loaded grammar from {args.grammar}")
    print(f"Using LLM model: {args.model}")
    print(f"Available vocabularies: {', '.join(vocabulary_manager.get_allowed_extensions())}")
    
    while True:
        # Get user input
        query = input("\nEnter your query (or 'q' to quit): ")
        
        if query.lower() in ['q', 'quit', 'exit']:
            break
        
        # Check dependencies
        all_available, missing_vocabs = vocabulary_manager.check_dependencies(query)
        
        if not all_available:
            print(f"Missing vocabularies: {', '.join(missing_vocabs)}.")
            print("Please import them before proceeding.")
            continue
        
        # Retrieve relevant examples
        print("\nRetrieving relevant examples...")
        retrieved_knowledge = retriever.retrieve(query)
        
        # Create instruction prompt
        instruction_prompt = 'You are an OML code generation assistant. Use only the following context to generate syntactically correct OML code:\n\n'
        
        # Add vocabulary restrictions
        vocab_restrictions = vocabulary_manager.format_vocabulary_restrictions()
        instruction_prompt += vocab_restrictions + "\n\n"
        
        # Add retrieved knowledge
        for example, score in retrieved_knowledge:
            instruction_prompt += f"EXAMPLE:\n{example}\n\n"
        
        # Generate and refine code
        print("\nGenerating OML code...")
        code, iterations, success = feedback_loop.generate_and_refine(query, instruction_prompt)
        
        if success:
            print(f"\nSuccessfully generated valid OML code after {iterations} iterations.")
        else:
            print(f"\nFailed to generate valid OML code after {iterations} iterations.")
        
        # Save generated code
        if code:
            output_file = f"generated_oml_{len(query.split())}.oml"
            with open(output_file, 'w') as file:
                file.write(code)
            print(f"Saved generated code to {output_file}")
    
    print("\nThank you for using OML Copilot!")
    
if __name__ == "__main__":
    main()
