#!/usr/bin/env python3
"""
Script to build examples database from OML files
"""

import os
import sys
import json
import argparse
import glob

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.rag.embeddings import EmbeddingManager
from src.rag.examples_processor import ExamplesProcessor

def main():
    parser = argparse.ArgumentParser(description='Build examples database from OML files')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input directory with OML files')
    parser.add_argument('--output', '-o', type=str, required=True, help='Output JSONL file')
    parser.add_argument('--embeddings', '-e', action='store_true', help='Generate embeddings')
    args = parser.parse_args()
    
    # Check if input directory exists
    if not os.path.isdir(args.input):
        print(f"Error: Input directory {args.input} does not exist")
        return 1
    
    # Find all OML files
    oml_files = glob.glob(os.path.join(args.input, "**/*.oml"), recursive=True)
    
    if not oml_files:
        print(f"No OML files found in {args.input}")
        return 1
    
    print(f"Found {len(oml_files)} OML files")
    
    # Process each file
    examples = []
    for i, file_path in enumerate(oml_files, 1):
        print(f"Processing file {i}/{len(oml_files)}: {file_path}")
        
        # Read file content
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Extract file name and directory
        file_name = os.path.basename(file_path)
        dir_name = os.path.basename(os.path.dirname(file_path))
        
        # Create example
        example = {
            'id': f"{dir_name}_{file_name}_{i}",
            'title': f"{dir_name} {file_name}",
            'description': f"OML vocabulary from {dir_name}",
            'tags': [dir_name, file_name.split('.')[0]],
            'input': f"Create an OML vocabulary for {dir_name} with {file_name.split('.')[0]}",
            'output': content
        }
        
        examples.append(example)
    
    # Save examples to JSONL file
    with open(args.output, 'w') as file:
        for example in examples:
            file.write(json.dumps(example) + '\n')
    
    print(f"Saved {len(examples)} examples to {args.output}")
    
    # Generate embeddings if requested
    if args.embeddings:
        print("Generating embeddings...")
        
        embedding_manager = EmbeddingManager()
        examples_processor = ExamplesProcessor(embedding_manager)
        
        # Load examples
        loaded_examples = examples_processor.load_examples(args.output)
        
        # Split large examples
        expanded_examples = examples_processor.split_large_examples(loaded_examples)
        
        # Process examples
        vector_db = examples_processor.process_examples(expanded_examples)
        
        # Save processed examples
        embedding_output = args.output.replace('.jsonl', '_embeddings.json')
        examples_processor.save_processed_examples(vector_db, embedding_output)
        
        print(f"Saved embeddings to {embedding_output}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
