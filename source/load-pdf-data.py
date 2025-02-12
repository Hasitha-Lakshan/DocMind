import ollama
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import psycopg
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Ollama client
client = ollama.Client(host='http://host.docker.internal:11434')

# PDF Loader
loader = PyMuPDFLoader("../input_files/PwC LLP Data.pdf")

def get_embedding(ollama_client, text):
    """Generate embeddings for a given text using Ollama."""
    try:
        response = ollama_client.embed(model='nomic-embed-text', input=text)
        return response['embeddings'][0] 
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return None

def load_data():
    """Load and process PDF data, then store it in PostgreSQL."""
    try:
        documents = loader.load()
        print(f'Number of Documents: {len(documents)}')

        # Split documents into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)
        print(f'Total text chunks: {len(docs)}')

        # Database connection parameters
        conn_params = {
            'dbname': os.getenv('POSTGRES_DB'),
            'user': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD'),
            'host': 'docmind_db',  # Docker service name
            'port': os.getenv('POSTGRES_PORT', '5432')
        }

        # Establish connection
        with psycopg.connect(**conn_params) as conn:
            with conn.cursor() as cursor:
                for doc in docs:
                    source = doc.metadata.get('source', 'Unknown')
                    page_number = doc.metadata.get('page', 0)
                    content = doc.page_content
                    embedding = get_embedding(client, content)

                    if embedding:
                        cursor.execute(
                            """
                            INSERT INTO dev.pdf_data (source, page_content, page_number, page_content_embeddings)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (source, content, page_number, embedding)
                        )

                conn.commit()
                print("Data successfully inserted into the database.")

    except Exception as error:
        print(f"Error: {error}")

# Run script
if __name__ == "__main__":
    load_data()
