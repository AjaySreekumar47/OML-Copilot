"""
OML-Copilot package initialization.

This package exposes the main retrieval, embedding, prompt engineering,
example processing, and dependency extraction utilities used by the
OML-Copilot workflow.
"""

from src.retriever import OMLRetriever
from src.embeddings import EmbeddingManager
from src.tokenizer_utils import get_tokenizer, count_tokens, truncate_text
from src.prompt_engineering import create_instruction_prompt, extract_oml_code
from src.examples_processor import ExamplesProcessor
from src.dependency_extractor import DependencyExtractor

__all__ = [
    "OMLRetriever",
    "EmbeddingManager",
    "get_tokenizer",
    "count_tokens",
    "truncate_text",
    "create_instruction_prompt",
    "extract_oml_code",
    "ExamplesProcessor",
    "DependencyExtractor",
]