# OML-Copilot Workflow

This document details the step-by-step workflow of the OML-Copilot system, from initial user request to final valid OML code generation.

## User Request Processing

### 1. User Input
The workflow begins when a user provides a natural language request through the VS Code interface:
- Simple requests: "Create a vocabulary for musical instruments"
- Complex requests: "Develop an OML vocabulary for describing various types of drilling missions which extends the mission, base, project and analysis vocabularies"

### 2. IDE Context Analysis
The system examines the user's workspace to gather essential context:
- OML files currently open in the editor
- Available vocabulary files in the project
- Dependencies defined in project configuration

### 3. Request Classification
The system categorizes the request based on complexity:
- **Simple Vocabulary Creation**: New vocabulary without specific dependencies
- **Extension Request**: New vocabulary extending existing ones
- **Complex Modeling**: Vocabulary with multiple concepts, relations, and constraints

## Knowledge Retrieval

### 4. Query Embedding
- User query is converted to vector representation using multilingual-E5-large-instruct model
- This embedding captures the semantic meaning of the request

### 5. Example Retrieval
- System searches the examples database using cosine similarity between query embedding and stored examples
- Top matches (typically 3-5) are selected based on relevance score
- Examples are tokenized and truncated to fit within model context window

### 6. Vocabulary Analysis
- System identifies which vocabularies are available in the workspace
- For extension requests, it verifies that required vocabularies are accessible
- If required vocabularies are missing, user is prompted to import them

## Code Generation

### 7. Prompt Construction
A structured prompt is assembled with:
- System instructions specifying OML generation task
- Available vocabulary definitions and constraints
- Retrieved example OML code snippets
- User query
- Previous error feedback (if this is a regeneration attempt)

### 8. Initial Generation
- Prompt is sent to Mistral LLM
- Model generates candidate OML code
- Output is extracted and formatted

### 9. Syntax Validation
- Generated code is parsed using Lark grammar parser
- Parser identifies any syntax violations
- If valid, code proceeds to final delivery
- If invalid, specific error information is extracted

## Error Handling and Regeneration

### 10. Error Analysis
When validation fails:
- System identifies the specific error location (line, column)
- Keywords or constructs causing errors are extracted
- System searches for examples of correct usage of these constructs

### 11. Feedback Formulation
A debugging prompt is created with:
- Original user request
- Previous generated code
- Specific error details
- Examples of correct construct usage
- Instructions for correction

### 12. Regeneration
- Updated prompt is sent back to LLM
- New code is generated with consideration of error feedback
- Validation process repeats
- This cycle continues up to 3 times or until valid code is produced

## Final Delivery

### 13. Result Presentation
- Valid OML code is presented to the user in the editor
- System provides explanatory comments within the code
- Optional annotations highlight key structures

### 14. Implementation Support
- User can modify or extend the generated code
- System remains available for additional queries about the generated code
- Generated code can be directly saved to project files

## Special Workflows

### Dependency Resolution
When missing dependencies are detected:
1. User is notified of required vocabularies
2. Options are provided to:
   - Import from standard libraries
   - Provide custom vocabulary paths
   - Generate minimal required vocabulary definitions

### Iterative Refinement
For complex modeling tasks:
1. System generates core vocabulary structure first
2. User can request progressive enhancement:
   - "Add a classification system for instruments"
   - "Include relations between instruments and musicians"
3. Each enhancement builds on previous valid code

### Grammar-Directed Generation
For challenging syntax constructs:
1. System identifies patterns that frequently cause errors
2. Specialized templates are applied for these constructs
3. Generation is constrained to follow validated patterns
