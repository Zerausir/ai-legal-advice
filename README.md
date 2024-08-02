# PAS Analysis Generator

This project generates analysis reports for Procedimiento Administrativo Sancionatorio (PAS) cases using Google's Vertex
AI.

## Description

The PAS Analysis Generator is a Python script that automates the process of analyzing PDF documents related to PAS
cases. It uses Google's Vertex AI to generate comprehensive reports based on the content of these documents.

## Features

- Automatic retrieval of relevant PDF files for a given PAS case
- Integration with Google Vertex AI for intelligent content analysis
- Generation of detailed reports in DOCX format
- Progress tracking during report generation

## Prerequisites

- Python 3.7+
- Google Cloud account with Vertex AI API enabled
- Service account key file with necessary permissions

## Installation

1. Clone the repository: git clone https://github.com/Zerausir/ai-legal-advice.git
2. Install required packages: pip install -r requirements.txt
3. Set up your `.env` file with the necessary environment variables (see Configuration section).

## Configuration

Create a `.env` file in the project root with the following variables:

- BASE_PATH=<path_to_base_folder>
- GOOGLE_MODEL=<google_model_name>
- LOCATION=<google_cloud_location>
- PROJECT_ID=<google_cloud_project_id>
- DOWNLOAD_FOLDER=<path_to_download_folder>
- KEY=<path_to_service_account_key_file>
- TEXT_SI=<system_instruction_text>
- TEXT_PROMPT=<initial_prompt_text>

Ensure that `TEXT_SI` and `TEXT_PROMPT` are enclosed in triple quotes if they contain multiple lines.

## Usage

Run the script: python main.py

Follow the prompts to enter the year and PAS number for analysis.

## PAS Folder Structure

The script expects a specific folder structure for each PAS case:

BASE_PATH/
├── YYYY_PAS_NUMBER/
│ ├── contestacion.pdf
│ ├── informe_tecnico.pdf
│ ├── acto_inicio.pdf
│ └── ejemplo_respuesta.pdf
├── reglamento.pdf
└── ley.pdf

Where:

- `YYYY` is the four-digit year
- `NUMBER` is the PAS case number
- `BASE_PATH` is set in your `.env` file

The script will look for the following files:

- PAS-specific files (in the YYYY_PAS_NUMBER folder):
    - contestacion.pdf
    - informe_tecnico.pdf
    - acto_inicio.pdf
    - ejemplo_respuesta.pdf
- Common files (in the BASE_PATH):
    - reglamento.pdf
    - ley.pdf

Ensure all these files are present for the script to run successfully.

## File Structure

- `main.py`: Main script for PAS analysis generation
- `requirements.txt`: List of Python package dependencies
- `.env`: Configuration file for environment variables

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Google Vertex AI for providing the generative AI capabilities
- Python-docx for DOCX file generation