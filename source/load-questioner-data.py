import os
from dotenv import load_dotenv
import psycopg
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Path to your Excel file
excel_file = os.path.join("input_files", "Questioner.xlsx")

def insert_initial_data():
    """Insert initial data into the database using psycopg and Excel data."""
    try:
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
                
                # Insert data for domain
                df_domain = pd.read_excel(excel_file, sheet_name='domain')
                for _, row in df_domain.iterrows():
                    cursor.execute("""
                        INSERT INTO dev.domain (domain_id, domain_name) VALUES (%s, %s)
                        ON CONFLICT (domain_id) DO NOTHING;
                    """, (row['domain_id'], row['domain_name']))

                # Insert data for sub_domain
                df_sub_domain = pd.read_excel(excel_file, sheet_name='sub_domain')
                for _, row in df_sub_domain.iterrows():
                    cursor.execute("""
                        INSERT INTO dev.sub_domain (sub_domain_id, sub_domain_name, domain_id) VALUES (%s, %s, %s)
                        ON CONFLICT (sub_domain_id) DO NOTHING;
                    """, (row['sub_domain_id'], row['sub_domain_name'], row['domain_id']))

                # Insert data for question
                df_question = pd.read_excel(excel_file, sheet_name='question')
                for _, row in df_question.iterrows():
                    cursor.execute("""
                        INSERT INTO dev.question (question_id, question, sub_domain_id) VALUES (%s, %s, %s)
                        ON CONFLICT (question_id) DO NOTHING;
                    """, (row['question_id'], row['queston'], row['sub_domain_id']))

                # Insert data for guidance
                df_guidance = pd.read_excel(excel_file, sheet_name='guidance')
                for _, row in df_guidance.iterrows():
                    cursor.execute("""
                        INSERT INTO dev.guidance (guidance_id, guidance) VALUES (%s, %s)
                        ON CONFLICT (guidance_id) DO NOTHING;
                    """, (row['guidance_id'], row['guidance']))

                # Insert data for question_guidance
                df_question_guidance = pd.read_excel(excel_file, sheet_name='question_guidance')
                for _, row in df_question_guidance.iterrows():
                    cursor.execute("""
                        INSERT INTO dev.question_guidance (question_id, guidance_id) VALUES (%s, %s)
                        ON CONFLICT (question_id, guidance_id) DO NOTHING;
                    """, (row['question_id'], row['guidance_id']))

                # Insert data for supporting_evidence
                df_supporting_evidence = pd.read_excel(excel_file, sheet_name='supporting_evidence')
                for _, row in df_supporting_evidence.iterrows():
                    cursor.execute("""
                        INSERT INTO dev.supporting_evidence (evidence_id, evidence, question_id) VALUES (%s, %s, %s)
                        ON CONFLICT (evidence_id) DO NOTHING;
                    """, (row['evidence_id'], row['evidence'], row['question_id']))

                # Insert data for status_guidance_of_question
                df_status_guidance = pd.read_excel(excel_file, sheet_name='status_guidance_of_question')
                for _, row in df_status_guidance.iterrows():
                    cursor.execute("""
                        INSERT INTO dev.status_guidance_of_question (status_guidance_id, guidance, status, question_id) VALUES (%s, %s, %s, %s)
                        ON CONFLICT (status_guidance_id) DO NOTHING;
                    """, (row['status_guidance_id'], row['guidance'], row['status'], row['question_id']))

                conn.commit()
                print("Data successfully inserted into the database.")
    
    except Exception as error:
        print(f"Error: {error}")

# Run script
if __name__ == "__main__":
    insert_initial_data()
