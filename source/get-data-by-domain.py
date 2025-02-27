import psycopg
from psycopg import sql
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

if __name__ == "__main__":
    domain_id_input = input("Enter the domain_id: ")
    domain_data = get_data_by_domain_id(domain_id_input)
    print(domain_data)
