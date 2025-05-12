# OML-Copilot Architecture

## System Overview

OML-Copilot is built on a modular architecture that combines state-of-the-art large language models, retrieval-augmented generation, and formal grammar validation. This document outlines the key components and their interactions.

## Architectural Components

### 1. User Interface Layer
- **VS Code Extension**: Integration with Continue extension provides a familiar interface for systems engineers
- **Input Processing**: Converts natural language queries and context from the OML IDE workspace into structured requests
- **Output Rendering**: Presents generated OML code, validation feedback, and suggestions

### 2. Core Processing Layer
- **LLM Component**: Leverages Mistral (7B parameters) to understand intent and generate initial OML code
- **RAG System**: Retrieves relevant examples from a curated collection of OML code snippets
- **Grammar Validation**: Uses Lark parser to validate syntax against formal OML grammar rules
- **Feedback Loop**: Processes validation errors and regenerates improved code versions

### 3. Knowledge Layer
- **OML Examples Database**: Structured collection of 301+ valid OML vocabulary examples
- **Grammar Rules**: Formal EBNF grammar translated to Lark format for validation
- **Embedding Models**: Sentence Transformer and CodeBERT for semantic similarity matching 
- **Vocabulary Dependencies**: Mapping of dependencies between OML vocabularies

## Data Flow

1. **Input Phase**:
   - User provides natural language request for OML code
   - System analyzes IDE workspace to determine available vocabularies
   
2. **Context Retrieval**:
   - Query is embedded using Sentence Transformer model
   - System retrieves most relevant examples based on semantic similarity
   - Available vocabularies are identified for dependency management

3. **Generation Phase**:
   - Prompt combining user request, retrieved examples, and available vocabularies is sent to LLM
   - LLM generates candidate OML code

4. **Validation Phase**:
   - Generated code is parsed with Lark grammar 
   - If valid, code is returned to user
   - If invalid, specific errors are identified

5. **Refinement Phase** (if needed):
   - Error information and example corrections are added to context
   - Updated prompt is sent back to LLM
   - New code is generated and validated
   - Process repeats until valid code is produced or maximum attempts reached

## Key Technical Decisions

### LLM Selection
Mistral 7B was selected for its balance of:
- Sufficient parameter count for understanding complex instructions
- Reasonable inference speed on commodity hardware
- Strong performance in code generation tasks

### Embedding Models
- **Multilingual-E5-large-instruct**: Used for query embedding due to strong performance on natural language understanding
- **CodeBERT**: Used for code embedding to capture programming language semantics

### Similarity Search Optimization
- **Tiered approach**: First search by semantic similarity, then by code structure
- **Tokenization**: Cl100k_base tokenizer limits context window to ensure relevant examples fit within model context

### Grammar Validation
- **Lark Parser**: Selected for efficient parsing and detailed error reporting
- **EBNF Translation**: Full OML grammar translated to Lark format through manual rule conversion

## Architectural Diagrams

### High-Level Architecture
![High-Level Architecture](images/high-level-architecture.png)

### Workflow Diagram
![Workflow Diagram](images/workflow-diagram.png)

### RAG Process
![RAG Process](images/rag-process.png)

## Future Architecture Enhancements

- **Fine-tuned Models**: Custom-trained models specialized for OML generation
- **Multi-step Reasoning**: Breaking complex modeling tasks into sub-problems
- **User Feedback Integration**: Learning from explicit user corrections
- **Collaborative Filtering**: Recommending patterns based on common usage across projects
- **Integration with OML Reasoning Tools**: Direct connection to validation and reasoning tools
