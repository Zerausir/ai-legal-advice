import os
import base64
import vertexai
from google.oauth2.service_account import Credentials
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
from docx import Document
from tqdm import tqdm
from environs import Env

env = Env()
env.read_env()

# Get environment variables
base_path = env("BASE_PATH")
google_model = env("GOOGLE_MODEL")
location = env("LOCATION")
project_id = env("PROJECT_ID")
download_folder = env("DOWNLOAD_FOLDER")
key = env("KEY")
text_si = env("TEXT_SI")
text_prompt = env("TEXT_PROMPT")


def get_pdf_files(base_path, year, pas_number):
    pas_folder = f"{year}_PAS_{pas_number}"
    full_path = os.path.join(base_path, pas_folder)

    # Required files
    pas_specific_files = [
        'contestacion.pdf',
        'informe_tecnico.pdf',
        'acto_inicio.pdf',
        'ejemplo_respuesta.pdf'
    ]
    common_files = [
        'reglamento.pdf',
        'ley.pdf'
    ]

    existing_files = []

    # Verify PAS-specific files
    for file in pas_specific_files:
        file_path = os.path.join(full_path, file)
        if os.path.exists(file_path):
            existing_files.append(file_path)
        else:
            print(f"Advertencia: El archivo {file} no existe en {full_path}")

    # Verify common files
    for file in common_files:
        file_path = os.path.join(base_path, file)
        if os.path.exists(file_path):
            existing_files.append(file_path)
        else:
            print(f"Advertencia: El archivo común {file} no existe en {base_path}")

    return existing_files if len(existing_files) == len(pas_specific_files) + len(common_files) else None


def generate(pdf_files):
    # Create a credentials object explicitly
    creds = Credentials.from_service_account_file(key)

    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location, credentials=creds)

    model = GenerativeModel(
        google_model,
        system_instruction=[text_si]
    )

    parts = [
        Part.from_text(text_prompt)]

    for pdf_file in pdf_files:
        file_name = os.path.basename(pdf_file)
        with open(pdf_file, 'rb') as file:
            pdf_data = file.read()
            encoded_pdf = base64.b64encode(pdf_data).decode('utf-8')
            parts.append(Part.from_text(f"Archivo: {file_name}"))
            parts.append(Part.from_data(
                mime_type="application/pdf",
                data=base64.b64decode(encoded_pdf)
            ))

    responses = model.generate_content(
        parts,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    # Prepare Word document
    doc = Document()
    analysis_text = ""

    # Process responses and update progress bar
    with tqdm() as pbar:
        for response in responses:
            analysis_text += response.text
            pbar.update(1)

    # Write analysis to Word document and handle potential errors
    try:
        # Create unique filename based on year and PAS number
        filename = f"Respuesta_PAS_{year}_{pas_number}.docx"
        full_filepath = os.path.join(download_folder, filename)

        doc.add_paragraph(analysis_text)
        doc.save(full_filepath)
        print(f"Análisis guardado exitosamente en {full_filepath}")
    except Exception as e:
        print(f"Error al guardar el documento Word: {e}")


# Define generation_config and safety_settings
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.8,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

if not base_path:
    print("Error: La variable de ambiente BASE_PATH no está definida.")
else:
    # Solicitar al usuario el año y número de PAS
    year = input("Ingrese el año (por ejemplo, 2024): ")
    pas_number = input("Ingrese el número de PAS: ")

    pdf_files = get_pdf_files(base_path, year, pas_number)

    if pdf_files:
        print(f"Se encontraron todos los archivos necesarios para el PAS {pas_number} del año {year}.")
        generate(pdf_files)
    else:
        print(
            f"No se encontraron todos los archivos necesarios para el PAS {pas_number} del año {year}. No se ejecutará el análisis.")
