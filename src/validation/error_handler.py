# error_handler.py - Error processing for feedback

import re

class ErrorHandler:
    def __init__(self, retriever=None):
        """
        Initialize the error handler.
        
        Args:
            retriever: Optional retriever for example lookup
        """
        self.retriever = retriever
        
    def process_error(self, oml_code, error_message):
        """
        Process an error and create debugging information.
        
        Args:
            oml_code (str): OML code with error
            error_message (str): Error message from parser
            
        Returns:
            dict: Structured error information
        """
        # Extract error details
        line_number, column_number, unexpected_token, expected_tokens = self.parse_error_details(error_message)
        
        # Extract the erroneous line from the OML code
        code_lines = oml_code.split("\n")
        error_line = code_lines[int(line_number) - 1] if line_number.isdigit() and int(line_number) <= len(code_lines) else "Unknown"
        
        # Extract the keyword from the line
        keyword = self.extract_keyword(error_line)
        
        # Retrieve example if retriever is available
        example = self.retrieve_example(keyword) if self.retriever else None
        
        # Create structured error info
        error_info = {
            'line_number': line_number,
            'column_number': column_number,
            'unexpected_token': unexpected_token,
            'expected_tokens': expected_tokens,
            'error_line': error_line,
            'keyword': keyword,
            'example': example
        }
        
        return error_info
    
    def format_debugging_prompt(self, error_info):
        """
        Format a debugging prompt from error information.
        
        Args:
            error_info (dict): Structured error information
            
        Returns:
            str: Formatted debugging prompt
        """
        debugging_prompt = f"""
        Error at line {error_info['line_number']}, column {error_info['column_number']}

        ### Erroneous Code:
        ```oml
        {error_info['error_line']}
        ```

        ### Suggested Fix:
        Ensure that {{}} are only used for the overall vocabulary definitions, and for no other subpart definition of the vocabulary.
        Check and ensure that all extensions are properly formatted to follow the correct schema, like: extends <link> as id
        The issue is likely due to incorrect usage of the **{error_info['keyword']}** keyword. Here's an example of correct usage:

        ```oml
        {error_info['example'] if error_info['example'] else 'Example not available.'}
        ```

        Adjust the structure accordingly and regenerate valid OML Code.
        """

        return debugging_prompt
    
    def parse_error_details(self, error_message):
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

        # Extract unexpected token (e.g., 'C' in "No terminal matches 'C'")
        unexpected_token_match = re.search(r"No terminal matches '(.+?)'", error_message)
        unexpected_token = unexpected_token_match.group(1) if unexpected_token_match else "Unknown"

        # Extract expected tokens list
        expected_tokens_match = re.findall(r'\* (\w+)', error_message)
        expected_tokens = ", ".join(expected_tokens_match) if expected_tokens_match else "Unknown"

        return line_number, column_number, unexpected_token, expected_tokens
    
    def extract_keyword(self, error_line):
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
    
    def retrieve_example(self, keyword):
        """
        Retrieve an example that correctly uses the keyword.
        
        Args:
            keyword (str): Keyword to find example for
            
        Returns:
            str: Example with keyword or None
        """
        if not self.retriever or not keyword:
            return None
            
        try:
            return self.retriever.retrieve_by_keyword(keyword)
        except Exception as e:
            print(f"Error retrieving example: {e}")
            return None
