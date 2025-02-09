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

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for discussion.

## License

This project is licensed under the MIT License.

