import psycopg
import ollama
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST")

def generate_embeddings(text):
    # Initialize Ollama client
    client = ollama.Client(host=OLLAMA_HOST)
    response = client.embed(model='nomic-embed-text', input=text)
    vetorized_search_query = response['embeddings'][0]
    return vetorized_search_query


def similarity_search_cosine_distance(query_text):
    # Database connection parameters
    conn_params = {
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': 'docmind_db',  # Docker service name
        'port': os.getenv('POSTGRES_PORT', '5432')
    }

    try:
        # Generate embedding for the query text
        query_embedding = generate_embeddings(query_text)

        # Establishing the connection using psycopg3
        with psycopg.connect(**conn_params) as conn:
            with conn.cursor() as cursor:
                # Performing the similarity search
                cursor.execute(
                    """
                    SELECT source, page_content, page_number
                    FROM dev.pdf_data
                    ORDER BY page_content_embeddings <=> %s::vector
                    LIMIT 3;
                    """,
                    (query_embedding,)
                )
                results = cursor.fetchall()
                
                # Printing the search results
                print("Similarity Search Results:")
                context_detail = ''
                for result in results:
                    context_detail += f"""
                    ####
                    Source 

                    {result[1]}

                    Source File= {result[0]}
                    Page Number= {result[2]}
                    
                    """
                
                return context_detail
    except Exception as error:
        print(f"Error: {error}")

def generate_answer_from_llm(query_text,query_context):
    system_prompt = """
    You are a helpful assistant.
    Multiple Context information with the source details like the source file name and page number. 
    You need to carefully analyze each given context information and then answer the user query accordingly.
    When you compile the answer you have to refer the original source file name and page number which you used to generate the answer. 
    If you can't find the details to answer the question, Please mention you don't know the answer.
    Final Answer should contain the Source File names and page numbers of the source details. 
    Final Answer should be formatted as below. 

    ##
    Answer: 

    ## References
    Source File Name: 
    Page Number:
    """
    
    user_prompt = f"""
    ###
    Context
    {query_context}

    ### User Query
    {query_text}
    """

    messages = [
        {
            'role': 'system',
            'content': system_prompt
        },
        {
            'role': 'user',
            'content': user_prompt
        }
    ]

    client = ollama.Client(host=OLLAMA_HOST)

    response = client.chat(
        'llama3.2:1b',
        messages=messages
    )

    print(response.message.content)

# Call the function to perform similarity search
if __name__ == "__main__":
    # Question
    query_text = "Describe Minimum data protection requirements applying to PwC LLP"
    print(f'\nUser Query:\n{query_text}\n')    
    # Getting the Information to setup the question answer context
    query_context = similarity_search_cosine_distance(query_text)

    print('\n\nFinal Answer: \n\n')
    # Generate the final answer
    generate_answer_from_llm(query_text=query_text,query_context=query_context)
