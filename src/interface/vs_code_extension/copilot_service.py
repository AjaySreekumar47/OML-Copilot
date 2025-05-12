# copilot_service.py - OML Copilot service for VS Code

import os
import json
from src.rag.retriever import OMLRetriever
from src.rag.embeddings import EmbeddingManager
from src.rag.examples_processor import ExamplesProcessor
from src.validation.validator import OMLValidator
from src.validation.error_handler import ErrorHandler
from src.validation.feedback_loop import FeedbackLoop
from src.dependency.vocabulary_manager import VocabularyManager

class OMLCopilotService:
    """Service that coordinates OML Copilot components for VS Code integration"""
    
    def __init__(self, workspace_path=None, examples_path=None, grammar_path=None, llm_client=None):
        """
        Initialize the OML Copilot service.
        
        Args:
            workspace_path (str): Path to workspace
            examples_path (str): Path to examples database
            grammar_path (str): Path to grammar file
            llm_client: LLM client for code generation
        """
        self.workspace_path = workspace_path
        
        # Set up embedding manager
        self.embedding_manager = EmbeddingManager()
        
        # Set up examples database
        self.examples_db = self._load_examples(examples_path)
        
        # Create retriever
        self.retriever = OMLRetriever(self.examples_db, self.embedding_manager)
        
        # Set up validator
        self.validator = OMLValidator(grammar_path)
        
        # Set up error handler
        self.error_handler = ErrorHandler(self.retriever)
        
        # Set up vocabulary manager
        self.vocabulary_manager = VocabularyManager(workspace_path)
        
        # Set up LLM client
        self.llm_client = llm_client
        
        # Set up feedback loop
        self.feedback_loop = FeedbackLoop(self.llm_client, self.validator, self.error_handler)
        
    def _load_examples(self, examples_path):
        """Load examples database"""
        if not examples_path or not os.path.exists(examples_path):
            return []
            
        processor = ExamplesProcessor(self.embedding_manager)
        examples = processor.load_examples(examples_path)
        return processor.process_examples(examples)
    
    def generate_oml_code(self, query):
        """
        Generate OML code for a query.
        
        Args:
            query (str): User query
            
        Returns:
            dict: Result with code and status
        """
        # Check dependencies
        all_available, missing_vocabs = self.vocabulary_manager.check_dependencies(query)
        
        if not all_available:
            return {
                'success': False,
                'message': f"Missing vocabularies: {', '.join(missing_vocabs)}.\nPlease import them before proceeding.",
                'code': None
            }
            
        # Retrieve relevant examples
        retrieved_knowledge = self.retriever.retrieve(query)
        
        # Create instruction prompt
        instruction_prompt = self._create_instruction_prompt(query, retrieved_knowledge)
        
        # Generate and refine code
        code, iterations, success = self.feedback_loop.generate_and_refine(query, instruction_prompt)
        
        return {
            'success': success,
            'message': f"Generated code after {iterations} iterations.",
            'code': code
        }
    
    def _create_instruction_prompt(self, query, retrieved_knowledge):
        """Create instruction prompt with retrieved knowledge and vocabulary restrictions"""
        base_prompt = 'You are an OML code generation assistant. Use only the following context to generate syntactically correct OML code:\n\n'
        
        # Add vocabulary restrictions
        vocab_restrictions = self.vocabulary_manager.format_vocabulary_restrictions()
        base_prompt += vocab_restrictions + "\n\n"
        
        # Add retrieved knowledge
        for example, score in retrieved_knowledge:
            base_prompt += f"EXAMPLE:\n{example}\n\n"
            
        return base_prompt
    
    def validate_oml_code(self, code):
        """
        Validate OML code.
        
        Args:
            code (str): OML code to validate
            
        Returns:
            dict: Validation result
        """
        is_valid, result = self.validator.validate(code)
        
        if is_valid:
            return {
                'valid': True,
                'message': "Code is valid.",
                'tree': str(result)
            }
        else:
            error_info = self.error_handler.process_error(code, str(result))
            return {
                'valid': False,
                'message': str(result),
                'error_info': error_info
            }
