# feedback_loop.py - Iterative feedback and regeneration

import time

class FeedbackLoop:
    def __init__(self, llm_client, validator, error_handler, max_iterations=3):
        """
        Initialize the feedback loop.
        
        Args:
            llm_client: LLM client for code generation
            validator: OML validator
            error_handler: Error handler for feedback
            max_iterations (int): Maximum iterations
        """
        self.llm_client = llm_client
        self.validator = validator
        self.error_handler = error_handler
        self.max_iterations = max_iterations
        
    def generate_and_refine(self, query, instruction_prompt=None):
        """
        Generate OML code and refine through feedback.
        
        Args:
            query (str): User query
            instruction_prompt (str): Optional instruction prompt
            
        Returns:
            tuple: (final_code, iterations, successful)
        """
        iterations = 0
        previous_code = None
        previous_error = None
        
        while iterations < self.max_iterations:
            # Create messages
            messages = [
                {'role': 'system', 'content': instruction_prompt or "You are an OML code generation assistant."},
                {'role': 'user', 'content': query}
            ]
            
            # Add debugging info from previous iteration if available
            if previous_code and previous_error:
                error_info = self.error_handler.process_error(previous_code, previous_error)
                debugging_prompt = self.error_handler.format_debugging_prompt(error_info)
                messages.append({'role': 'system', 'content': debugging_prompt})
            
            # Generate response
            print(f"\nAttempt {iterations + 1}/{self.max_iterations}...")
            response = self.generate_response(messages)
            
            # Extract code
            oml_code = self.validator.extract_code_from_response(response)
            
            if not oml_code:
                print("No OML code found in response")
                iterations += 1
                continue
                
            # Validate code
            is_valid, result = self.validator.validate(oml_code)
            
            if is_valid:
                print("\nValid OML code generated!")
                return oml_code, iterations + 1, True
            else:
                print(f"\nInvalid OML code. Error: {result}")
                previous_code = oml_code
                previous_error = result
                iterations += 1
                
        # Max iterations reached
        print(f"\nMaximum iterations ({self.max_iterations}) reached without success.")
        return previous_code, iterations, False
    
    def generate_response(self, messages):
        """
        Generate response from LLM.
        
        Args:
            messages (list): List of message dictionaries
            
        Returns:
            str: LLM response
        """
        try:
            # Stream response for better user experience
            full_response = ""
            for chunk in self.llm_client.chat(
                model="mistral",  # Or dynamic model parameter
                messages=messages,
                stream=True
            ):
                message = chunk['message']['content']
                full_response += message
                print(message, end='', flush=True)
                
            return full_response
        except Exception as e:
            print(f"Error generating response: {e}")
            # Fallback - non-streaming response
            response = self.llm_client.chat(model="mistral", messages=messages)
            return response['message']['content']
