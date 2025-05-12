# tokenizer_utils.py - Tokenization with tiktoken

import tiktoken

def get_tokenizer(encoding_name="cl100k_base"):
    """
    Get a tokenizer for the specified encoding.
    
    Args:
        encoding_name (str): Name of the encoding to use
        
    Returns:
        Tokenizer: Tiktoken tokenizer
    """
    return tiktoken.get_encoding(encoding_name)

def count_tokens(text, tokenizer=None):
    """
    Count the number of tokens in text.
    
    Args:
        text (str): Text to count tokens for
        tokenizer: Optional tokenizer (creates one if not provided)
        
    Returns:
        int: Number of tokens
    """
    if tokenizer is None:
        tokenizer = get_tokenizer()
        
    return len(tokenizer.encode(text))

def truncate_text(text, max_tokens, tokenizer=None):
    """
    Truncate text to fit within token limit.
    
    Args:
        text (str): Text to truncate
        max_tokens (int): Maximum tokens allowed
        tokenizer: Optional tokenizer (creates one if not provided)
        
    Returns:
        str: Truncated text
    """
    if tokenizer is None:
        tokenizer = get_tokenizer()
        
    tokens = tokenizer.encode(text)
    if len(tokens) > max_tokens:
        truncated_tokens = tokens[:max_tokens]
        return tokenizer.decode(truncated_tokens)
    return text

def fit_examples_in_context(examples, system_prompt, max_tokens=4096, tokenizer=None):
    """
    Fit as many examples as possible within context window.
    
    Args:
        examples (list): List of (text, score) tuples
        system_prompt (str): System prompt text
        max_tokens (int): Maximum context window size
        tokenizer: Optional tokenizer
        
    Returns:
        list: List of examples that fit in context
    """
    if tokenizer is None:
        tokenizer = get_tokenizer()
        
    # Count tokens in system prompt
    system_tokens = count_tokens(system_prompt, tokenizer)
    
    # Reserve some tokens for user query and LLM response
    available_tokens = max_tokens - system_tokens - 500  # Reserve 500 for query/response
    
    fitted_examples = []
    tokens_used = 0
    
    for example, score in examples:
        example_tokens = count_tokens(example, tokenizer)
        
        if tokens_used + example_tokens <= available_tokens:
            fitted_examples.append((example, score))
            tokens_used += example_tokens
        else:
            break
            
    return fitted_examples
