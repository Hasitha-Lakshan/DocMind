import psycopg
from psycopg import sql
import os
import ollama
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


OLLAMA_HOST = os.getenv("OLLAMA_HOST")

def get_data_by_domain_id(domain_id):
    # Connect to the PostgreSQL database
    conn = psycopg.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST', 'docmind_db'),  # Docker service name or localhost
        port=os.getenv('POSTGRES_PORT', '5432')
    )
    
    cursor = conn.cursor()

    try:
        # Initialize the JSON structure
        result = {}

        # Get domain details
        cursor.execute("""
            SELECT domain_id, domain_name
            FROM dev.domain
            WHERE domain_id = %s
        """, (domain_id,))
        domain = cursor.fetchone()

        if not domain:
            print("No domain found with the given domain_id.")
            return
        
        result["domain"] = {
            "id": domain[0],
            "name": domain[1],
            "sub_domains": []
        }

        # Get sub_domains for the domain
        cursor.execute("""
            SELECT sub_domain_id, sub_domain_name
            FROM dev.sub_domain
            WHERE domain_id = %s
        """, (domain_id,))
        sub_domains = cursor.fetchall()

        for sub_domain in sub_domains:
            sub_domain_obj = {
                "id": sub_domain[0],
                "name": sub_domain[1],
                "questions": []
            }

            # Get questions for the sub_domain
            cursor.execute("""
                SELECT question_id, question
                FROM dev.question
                WHERE sub_domain_id = %s
            """, (sub_domain[0],))
            questions = cursor.fetchall()

            for question in questions:
                question_obj = {
                    "id": question[0],
                    "text": question[1],
                    "guidances": [],
                    "evidences": [],
                    "status_guidances": []
                }

                # Get guidance for the question
                cursor.execute("""
                    SELECT g.guidance_id, g.guidance
                    FROM dev.guidance g
                    JOIN dev.question_guidance qg ON g.guidance_id = qg.guidance_id
                    WHERE qg.question_id = %s
                """, (question[0],))
                guidances = cursor.fetchall()

                for guidance in guidances:
                    question_obj["guidances"].append({
                        "id": guidance[0],
                        "text": guidance[1]
                    })

                # Get supporting evidence for the question
                cursor.execute("""
                    SELECT evidence_id, evidence
                    FROM dev.supporting_evidence
                    WHERE question_id = %s
                """, (question[0],))
                evidences = cursor.fetchall()

                for evidence in evidences:
                    question_obj["evidences"].append({
                        "id": evidence[0],
                        "text": evidence[1]
                    })

                # Get status guidance for the question
                cursor.execute("""
                    SELECT status_guidance_id, guidance, status
                    FROM dev.status_guidance_of_question
                    WHERE question_id = %s
                """, (question[0],))
                status_guidances = cursor.fetchall()

                for status_guidance in status_guidances:
                    question_obj["status_guidances"].append({
                        "id": status_guidance[0],
                        "text": status_guidance[1],
                        "status": status_guidance[2]
                    })

                sub_domain_obj["questions"].append(question_obj)

            result["domain"]["sub_domains"].append(sub_domain_obj)

        # Convert the result to JSON format
        json_output = json.dumps(result, indent=4)
        return json_output

    except Exception as e:
        print("An error occurred:", e)
    finally:
        cursor.close()
        conn.close()


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
                # print("Similarity Search Results:")
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

import json

def generate_answer_from_llm(query_text, query_context):
    system_prompt = """
    You are a helpful assistant.
    Multiple Context information with the source details like the source file name and page number. 
    You need to carefully analyze each given context information and then answer the user query accordingly.
    When you compile the answer you have to refer the original source file name and page number which you used to generate the answer. 
    If you can't find the details to answer the question, please mention you don't know the answer.
    The final output should be in JSON format as follows:

    {
        "response": "<Your Answer Here>",
        "reference": {
            "sourceFileName": "<Source File Name>",
            "pageNumber": <Page Number>
        }
    }
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

    # Extract the message content
    answer_content = response.message.content.strip()

    # Attempt to parse as JSON
    try:
        json_output = json.loads(answer_content)
    except json.JSONDecodeError:
        print("Error: Response is not valid JSON.")
        print("Response content:", answer_content)
        json_output = {
            "answer": "",
            "reference": {
                "sourceFileName": "",
                "pageNumber": 0
            }
        }

    return json_output



def transform_domain_data(domain_data):
    # Parse the JSON string into a dictionary
    data = json.loads(domain_data)

    # Initialize the new structure
    transformed_result = {
        "domain": {
            "sub_domains": []
        }
    }

    # Traverse the original structure
    if "domain" in data:
        transformed_result["domain"]["id"] = data["domain"]["id"]
        transformed_result["domain"]["name"] = data["domain"]["name"]

        for sub_domain in data["domain"].get("sub_domains", []):
            sub_domain_obj = {
                "id": sub_domain["id"],
                "name": sub_domain["name"],
                "questions": []
            }

            for question in sub_domain.get("questions", []):
                # Get the question text
                question_text = question["text"]
                
                # Get the context using similarity search
                context = similarity_search_cosine_distance(question_text)

                # Generate the answer using the context and question text
                answer = generate_answer_from_llm(question_text, context)
                
                question_obj = {
                    "question": question_text,
                    "answer": answer  # Store the generated answer
                }
                sub_domain_obj["questions"].append(question_obj)

            transformed_result["domain"]["sub_domains"].append(sub_domain_obj)

    # Convert the result to JSON format
    transformed_json = json.dumps(transformed_result, indent=4)
    return transformed_json


def write_json_to_file(data, domain_id, output_dir="/app/output"):
    """
    Writes JSON data to a file in the specified output directory.
    The file is named dynamically using the domain_id.

    Args:
        data (str): The JSON data to write.
        domain_id (str): The domain_id used to name the file.
        output_dir (str): The directory where the file will be saved.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct the file name and path
    file_name = f"transformed_data_{domain_id}.json"
    file_path = os.path.join(output_dir, file_name)
    
    # Write the data to the file
    with open(file_path, 'w') as json_file:
        json_file.write(data)
    
    print(f"Transformed data has been written to {file_path}")


if __name__ == "__main__":
    domain_id_input = input("Enter the domain_id: ")
    domain_data = get_data_by_domain_id(domain_id_input)
    
    # Transform the data
    transformed_data = transform_domain_data(domain_data)
    
    # Write the transformed data to a JSON file
    write_json_to_file(transformed_data, domain_id_input)

