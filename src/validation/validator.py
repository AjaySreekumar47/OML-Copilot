# validator.py - Grammar validation for OML code

from lark import Lark, UnexpectedInput
import os
import re

class OMLValidator:
    def __init__(self, grammar_file=None):
        """
        Initialize the OML validator with grammar.
        
        Args:
            grammar_file (str): Path to grammar file (defaults to standard location)
        """
        if grammar_file is None:
            # Default location
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            grammar_file = os.path.join(root_dir, "src", "grammar", "oml3_lark.txt")
            
        # Load the grammar
        with open(grammar_file, "r") as file:
            self.grammar_text = file.read()
            
        # Create the parser
        self.parser = Lark(self.grammar_text, start='ontology')  # Adjust start rule as needed
        
    def validate(self, oml_code):
        """
        Validate OML code against grammar.
        
        Args:
            oml_code (str): OML code to validate
            
        Returns:
            tuple: (is_valid, result) - Boolean and parse tree or error message
        """
        try:
            # Parse the generated code
            tree = self.parser.parse(oml_code)
            return True, tree  # Code is valid, return parse tree
        except UnexpectedInput as e:
            # If parsing fails, the code doesn't follow the grammar
            return False, str(e)  # Return error message
        except Exception as e:
            # Handle other exceptions
            return False, f"Validation error: {str(e)}"
            
    def extract_code_from_response(self, response):
        """
        Extract OML code from LLM response.
        
        Args:
            response (str): Full LLM response
            
        Returns:
            str: Extracted OML code or None
        """
        # Use case-insensitive pattern to match 'oml' or 'OML' at the start
        pattern = r'```(?:[a-zA-Z]+)?\n(.*?)```'
        match = re.search(pattern, response, re.DOTALL)
        if match:
            return match.group(1)
        else:
            # Try alternative pattern without language specifier
            pattern = r'```(.*?)```'
            match = re.search(pattern, response, re.DOTALL)
            if match:
                return match.group(1)
            return None
