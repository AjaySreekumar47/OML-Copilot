# examples_processor.py - Processing and storing examples

import json
import os
from src.rag.embeddings import EmbeddingManager
import tiktoken

class ExamplesProcessor:
    def __init__(self, embedding_manager=None):
        """
        Initialize the examples processor.
        
        Args:
            embedding_manager: Optional embedding manager instance
        """
        self.embedding_manager = embedding_manager or EmbeddingManager()
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
    def load_examples(self, file_path):
        """
        Load examples from a JSONL file.
        
        Args:
            file_path (str): Path to JSONL file
            
        Returns:
            list: Loaded examples
        """
        examples = []
        with open(file_path, 'r') as file:
            for line in file:
                examples.append(json.loads(line))
        print(f'Loaded {len(examples)} entries from {file_path}')
        return examples
    
    def process_examples(self, examples, max_tokens=4096):
        """
        Process examples and build vector database.
        
        Args:
            examples (list): List of example dictionaries
            max_tokens (int): Maximum tokens for truncation
            
        Returns:
            list: Vector database with embeddings
        """
        return self.embedding_manager.build_database(examples, self.tokenizer, max_tokens)
    
    def split_large_examples(self, examples, max_tokens=1000):
        """
        Split large examples into smaller chunks.
        
        Args:
            examples (list): List of example dictionaries
            max_tokens (int): Threshold for splitting
            
        Returns:
            list: Expanded list with split examples
        """
        expanded_examples = []
        
        for example in examples:
            input_text = example['input']
            output_text = example['output']
            
            # If output is small enough, keep as is
            if len(self.tokenizer.encode(output_text)) <= max_tokens:
                expanded_examples.append(example)
                continue
                
            # Split large examples
            output_lines = output_text.split('\n')
            current_chunk = []
            current_tokens = 0
            
            for line in output_lines:
                line_tokens = len(self.tokenizer.encode(line))
                
                if current_tokens + line_tokens > max_tokens:
                    # Create new example with current chunk
                    if current_chunk:
                        chunk_text = '\n'.join(current_chunk)
                        expanded_examples.append({
                            'id': f"{example['id']}_chunk{len(expanded_examples)}",
                            'title': example['title'],
                            'description': example['description'],
                            'tags': example['tags'],
                            'input': input_text,
                            'output': chunk_text
                        })
                    
                    # Start new chunk
                    current_chunk = [line]
                    current_tokens = line_tokens
                else:
                    current_chunk.append(line)
                    current_tokens += line_tokens
            
            # Add final chunk if not empty
            if current_chunk:
                chunk_text = '\n'.join(current_chunk)
                expanded_examples.append({
                    'id': f"{example['id']}_chunk{len(expanded_examples)}",
                    'title': example['title'],
                    'description': example['description'],
                    'tags': example['tags'],
                    'input': input_text,
                    'output': chunk_text
                })
                
        print(f'Split {len(examples)} examples into {len(expanded_examples)} chunks')
        return expanded_examples
    
    def save_processed_examples(self, vector_db, file_path):
        """
        Save processed examples to a file.
        
        Args:
            vector_db (list): Vector database
            file_path (str): Output file path
        """
        # Convert vector_db to serializable format
        serializable_db = []
        
        for input_text, output_text, input_embedding, output_embedding in vector_db:
            serializable_db.append({
                'input': input_text,
                'output': output_text,
                'input_embedding': input_embedding.tolist(),
                'output_embedding': output_embedding.tolist()
            })
            
        with open(file_path, 'w') as file:
            json.dump(serializable_db, file)
            
        print(f'Saved processed examples to {file_path}')
