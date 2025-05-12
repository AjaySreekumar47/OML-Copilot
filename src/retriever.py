# retriever.py - Core document retrieval functionality

import tiktoken
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class OMLRetriever:
    def __init__(self, vector_db, embedding_model, tokenizer=None, max_tokens=4096):
        """
        Initialize the OML retriever with a vector database and embedding model.
        
        Args:
            vector_db: Database of examples with embeddings
            embedding_model: Model for embedding queries
            tokenizer: Tokenizer for managing context length
            max_tokens: Maximum tokens for context window
        """
        self.vector_db = vector_db
        self.embedding_model = embedding_model
        self.tokenizer = tokenizer or tiktoken.get_encoding("cl100k_base")
        self.max_tokens = max_tokens
    
    def retrieve(self, query, top_n=3):
        """
        Retrieve the most relevant examples for a given query.
        
        Args:
            query (str): The query to find examples for
            top_n (int): Number of examples to retrieve
            
        Returns:
            list: Top N relevant examples with similarity scores
        """
        # Truncate query to token limit
        query = self._truncate_to_token_limit(query)

        # Use E5 model's query format for embedding
        query_embedding = self.embedding_model.encode(f"query: {query}")

        similarities = []
        for input_text, output_text, input_embedding, output_embedding in self.vector_db:
            # Calculate similarity
            similarity = self._calculate_cosine_similarity(query_embedding, input_embedding)
            similarities.append((output_text, similarity))

        # Sort by similarity in descending order
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Print the retrieved RAGs for debugging
        print("\nRetrieved RAGs:")
        for i, (output_text, similarity) in enumerate(similarities[:top_n]):
            # Truncate output for display
            display_text = self._truncate_to_token_limit(output_text, max_tokens=100)
            print(f"Rank {i+1}: Similarity = {similarity:.4f} -> {display_text}")

        # Return the top N most relevant outputs
        return similarities[:top_n]
    
    def retrieve_by_keyword(self, keyword):
        """
        Fetches an example statement that correctly uses the specified keyword.
        
        Args:
            keyword (str): The keyword to search for
            
        Returns:
            str: Example that uses the keyword
        """
        for input_text, output_text, _, _ in self.vector_db:
            if keyword and (keyword in input_text or keyword in output_text):
                return output_text  # Return the first relevant example found

        return "No relevant example found in the database."  # Fallback case
    
    def _calculate_cosine_similarity(self, a, b):
        """Calculate cosine similarity between two vectors."""
        dot_product = sum([x * y for x, y in zip(a, b)])
        norm_a = sum([x ** 2 for x in a]) ** 0.5
        norm_b = sum([x ** 2 for x in b]) ** 0.5
        return dot_product / (norm_a * norm_b)
    
    def _truncate_to_token_limit(self, text, max_tokens=None):
        """
        Truncate text to fit within the specified token limit.
        
        Args:
            text (str): Input text to truncate
            max_tokens (int): Maximum tokens (defaults to self.max_tokens)
            
        Returns:
            str: Truncated text
        """
        if max_tokens is None:
            max_tokens = self.max_tokens
            
        tokens = self.tokenizer.encode(text)
        if len(tokens) > max_tokens:
            truncated_tokens = tokens[:max_tokens]
            return self.tokenizer.decode(truncated_tokens)
        return text
