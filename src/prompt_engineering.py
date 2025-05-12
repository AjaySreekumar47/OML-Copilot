# prompt_engineering.py - Prompt templates and construction

import re
from src.rag.tokenizer_utils import truncate_text

def create_instruction_prompt(retrieved_knowledge, previous_oml_code=None, previous_error_message=None, max_tokens=4096):
    """
    Create an instruction prompt for the LLM using retrieved examples.
    
    Args:
        retrieved_knowledge (list): List of (example, similarity) tuples
        previous_oml_code (str): Previous generated code (for debugging)
        previous_error_message (str): Previous error message (for debugging)
        max_tokens (int): Maximum tokens for prompt
        
    Returns:
        str: Formatted instruction prompt
    """
    # Base instruction prompt
    instruction_prompt = 'You are an OML code generation assistant.\nUse only the following context to generate syntactically correct OML code:\n'

    # Add retrieved knowledge chunks, ensuring token limit
    for chunk, similarity in retrieved_knowledge:
        # Truncate each chunk
        truncated_chunk = truncate_text(chunk, 300)
        instruction_prompt += f' - {truncated_chunk}\n'

    # Add previous debugging info if available
    if previous_oml_code and previous_error_message:
        debugging_prompt = format_debugging_prompt(previous_oml_code, previous_error_message)
        instruction_prompt += "\n" + truncate_text(debugging_prompt, 500)

    # Truncate final instruction prompt
    return truncate_text(instruction_prompt, max_tokens)

def format_debugging_prompt(code, error_message):
    """
    Format a debugging prompt based on error details.
    
    Args:
        code (str): OML code with errors
        error_message (str): Error message from parser
        
    Returns:
        str: Formatted debugging prompt
    """
    # Extract details from the error message
    line_number, column_number, unexpected_token, expected_tokens = parse_error_details(error_message)

    # Extract the erroneous line from the OML code
    code_lines = code.split("\n")
    error_line = code_lines[int(line_number) - 1] if line_number.isdigit() and int(line_number) <= len(code_lines) else "Unknown"

    # Extract the keyword
    keyword = extract_keyword(error_line)

    # Create a debugging prompt
    debugging_prompt = f"""
    {error_message}

    ### Erroneous Code:
    ```oml
    {error_line}
    ```

    ### Suggested Fix:
    Ensure that {{}} are only used for the overall vocabulary definitions, and for no other subpart definition of the vocabulary.
    Check and ensure that all extensions are properly formatted to follow the correct schema, like: extends <link> as id
    The issue is likely due to incorrect usage of the **{keyword}** keyword. Here's an example of correct usage:

    ```oml
    [Example will be retrieved dynamically]
    ```

    Adjust the structure accordingly and regenerate valid OML Code.
    """

    return debugging_prompt

def parse_error_details(error_message):
    """
    Extract key details from parser error message.
    
    Args:
        error_message (str): Error message from parser
        
    Returns:
        tuple: Line number, column number, unexpected token, expected tokens
    """
    # Extract line and column number
    line_col_match = re.search(r'at line (\d+) col (\d+)', error_message)
    line_number, column_number = line_col_match.groups() if line_col_match else ("Unknown", "Unknown")

    # Extract unexpected token
    unexpected_token_match = re.search(r"No terminal matches '(.+?)'", error_message)
    unexpected_token = unexpected_token_match.group(1) if unexpected_token_match else "Unknown"

    # Extract expected tokens list
    expected_tokens_match = re.findall(r'\* (\w+)', error_message)
    expected_tokens = ", ".join(expected_tokens_match) if expected_tokens_match else "Unknown"

    return line_number, column_number, unexpected_token, expected_tokens

def extract_keyword(error_line):
    """
    Extract the keyword from an error line.
    
    Args:
        error_line (str): Line with error
        
    Returns:
        str: Extracted keyword
    """
    # Extract the first word (typically the keyword)
    first_word = error_line.strip().split(" ")[0]
    return first_word

def extract_oml_code(response):
    """
    Extract OML code from LLM response.
    
    Args:
        response (str): Full LLM response
        
    Returns:
        str: Extracted OML code or None
    """
    # Match code blocks with or without language specifier
    pattern = r'```(?:[a-zA-Z]+)?\n(.*?)```'
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1)
    else:
        return None
