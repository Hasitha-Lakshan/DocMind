# DocMind

## Overview

DocMind is an automated document validation tool that processes PDF files against predefined guidelines. It evaluates the content and structure of a PDF document to determine whether it aligns with specific criteria. Based on the analysis, it provides a checklist indicating compliance for each criterion, along with references to the relevant page or paragraph in the PDF.

## Features

- Extracts text and metadata from PDFs.
- Compares document contents against a set of predefined guidelines.
- Generates a compliance report with a detailed checklist.
- Provides references to the relevant pages or paragraphs for each criterion.
- Uses a combination of machine learning and rule-based validation.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Hasitha-Lakshan/DocMind.git
   cd DocMind
   ```
2. Build and run the Docker container:
   ```sh
   docker-compose up -d
   ```
3. Ensure dependencies are installed (if running without Docker):
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Place the PDF documents in the designated input directory.
2. Run the application:
   ```sh
   python main.py
   ```
3. The application will process the documents and generate a compliance checklist with references to the source content.

## Configuration

- The criteria for validation can be adjusted in the `config.yaml` file.
- Database connections and environment variables are defined in the `docker-compose.yml` file.

## Handling Environment Variables

To avoid storing sensitive credentials in `docker-compose.yml`, DocMind uses an `.env` file. Create a `.env` file in the project root with the following variables:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=docmind_db

REDIS_HOST=redis
REDIS_PORT=6379

ELASTICSEARCH_HOST=http://elasticsearch:9200

OLLAMA_HOST=http://ollama:11434

DATABASE_URL=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@postgres:5432/$POSTGRES_DB
```

Ensure your `.env` file is **not** included in version control by adding it to `.gitignore`.

Run the application with:
```sh
docker-compose --env-file .env up -d
```

## Development Guide

- **For code changes (e.g., Python files, configs loaded dynamically):**
  👉 No need to restart the container. Just save your file and rerun your script inside the container if needed:
  
  ```sh
  docker-compose exec docmind_app python main.py
  ```
  (or use `docker-compose logs -f` to check if it reloads automatically).

- **For dependency changes (e.g., requirements.txt):**
  👉 You must rebuild the container:
  
  ```sh
  docker-compose up --build -d
  ```

- **For configuration changes (e.g., docker-compose.yml, .env):**
  👉 Restart the affected service:
  
  ```sh
  docker-compose restart docmind_app
  ```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for discussion.

## License

This project is licensed under the MIT License.

