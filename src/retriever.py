import json
import ollama
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the JSONL dataset
dataset = []
with open('oml_examples.jsonl', 'r') as file:
    for line in file:
        dataset.append(json.loads(line))
    print(f'Loaded {len(dataset)} entries')

# Initialize the SentenceTransformer model
EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
LANGUAGE_MODEL = "mistral"  # The Mistral model you pulled

# VECTOR_DB to store input-output pairs and their embeddings
VECTOR_DB = []

# Function to add input-output pairs to the database with embeddings
def add_chunk_to_database(input_text, output_text):
    input_embedding = EMBEDDING_MODEL.encode([input_text])[0]  # Use SentenceTransformer for input embedding
    output_embedding = EMBEDDING_MODEL.encode([output_text])[0]  # Use SentenceTransformer for output embedding
    VECTOR_DB.append((input_text, output_text, input_embedding, output_embedding))

# Add all input-output pairs from the dataset to the VECTOR_DB
for i, example in enumerate(dataset):
    add_chunk_to_database(example['input'], example['output'])
    print(f'Added example {i+1}/{len(dataset)} to the database')

# Function to calculate cosine similarity between two vectors
def cosine_similarity(a, b):
    dot_product = sum([x * y for x, y in zip(a, b)])
    norm_a = sum([x ** 2 for x in a]) ** 0.5
    norm_b = sum([x ** 2 for x in b]) ** 0.5
    return dot_product / (norm_a * norm_b)

# Function to retrieve the top N most similar outputs based on the input query
def retrieve(query, top_n=3):
    query_embedding = EMBEDDING_MODEL.encode([query])[0]  # Get embedding for the query (input part)
    similarities = []
    for input_text, output_text, input_embedding, output_embedding in VECTOR_DB:
        similarity = cosine_similarity(query_embedding, input_embedding)  # Compare with input embeddings
        similarities.append((output_text, similarity))

    # Sort by similarity in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Return the top N most relevant outputs
    return similarities[:top_n]

# Chatbot interaction
# Create an OML vocabulary for describing different types of vehicles
input_query = input('Ask me a question: ')
retrieved_knowledge = retrieve(input_query)

print('Retrieved knowledge:')
for output_text, similarity in retrieved_knowledge:
    print(f' - (similarity: {similarity:.2f}) {output_text}')

# Construct the instruction prompt for the chatbot
instruction_prompt = '''You are a helpful chatbot.
Use only the following pieces of context to generate OML code.
Don't make up any new information about the structure and grammar of OML:
''' + '\n'.join([f' - {chunk}' for chunk, similarity in retrieved_knowledge])

# Stream the chatbot's response using the Mistral model
stream = ollama.chat(
    model=LANGUAGE_MODEL,
    messages=[
        {'role': 'system', 'content': instruction_prompt},
        {'role': 'user', 'content': input_query},
    ],
    stream=True,
)

response_content = ""  # Variable to store the response content

# Print and capture chatbot response in real-time
for chunk in stream:
    message = chunk['message']['content']
    response_content += message  # Append the chunk to the variable
    print(message, end='', flush=True)  # Print immediately with flush
