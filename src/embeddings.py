# embeddings.py - Embedding model implementation

from sentence_transformers import SentenceTransformer

class EmbeddingManager:
    def __init__(self, model_name='intfloat/multilingual-e5-large-instruct'):
        """
        Initialize the embedding manager with a specified model.
        
        Args:
            model_name (str): Name of the sentence transformer model to use
        """
        self.model = SentenceTransformer(model_name)
        
    def get_query_embedding(self, text):
        """
        Get embedding for a query text.
        
        Args:
            text (str): Query text
            
        Returns:
            numpy.ndarray: Embedding vector
        """
        return self.model.encode(f"query: {text}")
    
    def get_passage_embedding(self, text):
        """
        Get embedding for a passage/document text.
        
        Args:
            text (str): Passage text
            
        Returns:
            numpy.ndarray: Embedding vector
        """
        return self.model.encode(f"passage: {text}")
    
    def build_database(self, examples, tokenizer=None, max_tokens=4096):
        """
        Build a vector database from examples.
        
        Args:
            examples (list): List of examples as dicts with 'input' and 'output' keys
            tokenizer: Optional tokenizer for truncation
            max_tokens: Max tokens for truncation
            
        Returns:
            list: Vector database with input, output, and embeddings
        """
        vector_db = []
        
        for i, example in enumerate(examples):
            input_text = example['input']
            output_text = example['output']
            
            # Truncate if tokenizer provided
            if tokenizer:
                input_text = self._truncate_text(tokenizer, input_text, max_tokens)
                output_text = self._truncate_text(tokenizer, output_text, max_tokens)
            
            # Create embeddings
            input_embedding = self.get_query_embedding(input_text)
            output_embedding = self.get_passage_embedding(output_text)
            
            vector_db.append((input_text, output_text, input_embedding, output_embedding))
            print(f'Added example {i+1}/{len(examples)} to the database')
            
        return vector_db
    
    def _truncate_text(self, tokenizer, text, max_tokens):
        """Truncate text using tokenizer"""
        tokens = tokenizer.encode(text)
        if len(tokens) > max_tokens:
            return tokenizer.decode(tokens[:max_tokens])
        return text
