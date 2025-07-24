import subprocess
import os
import sys
from pathlib import Path
import openai
import tiktoken
import re
# Add dotenv to load environment variables from .env file
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

lang_dict = {
    "ar": "Arabic",
    # "zh": "Chinese",
    # "fr": "French",
    # "ru": "Russian",
    # "es": "Spanish",
    # "de": "German",
}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_type = "azure"
openai.api_base = "https://moc-translator.openai.azure.com/"
# openai.api_version = "2023-05-15"
openai.api_key = OPENAI_API_KEY

TARGET_LANGS = ['ar']  # Update as needed
# TARGET_LANGS = ['ru', 'es', 'it', 'fr', 'ar', 'zh', 'pt', 'de']  # Update as needed

EN_DIR = Path('documentation/docs/en')
BASE_DIR = Path('documentation/docs')
excluded_terms = [
    "wis2box",
    "WIS2 in a box",
    "Global Broker",
    "Global Cache",
    "Global Discovery Catalogue",
    "WCMP2",
    "WIS2 Node",
    "WIS2",
    "MQTT",
    "MQTT Explorer",
    "Google Cloud Platform",
    "Amazon Web Services",
    "WMO Core Metadata Profile 2",
    "Data Type",
    "Centre ID",
    "wis2box-webapp",
    "wis2box-management",
    "wis2box-api",
    "collections/stations",
    "processes/wis2box",
    "wis2box-incoming",
    "MinIO",
    "Grafana",
    "YOUR-HOST"
    "wiki",
]

# Token estimation
def estimate_token_count(text, model="gpt-4-turbo"):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

def get_changed_files():
    result = subprocess.run(
        ['git', 'diff', '--name-only', 'HEAD'],
        stdout=subprocess.PIPE,
        text=True,
        check=True
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip().endswith('.md')]

def estimate_token_count(text):
    # Simple approximation: 1 token ≈ 4 characters (adjust as needed)
    return max(1, len(text) // 4)

def split_markdown_into_blocks(text):
    """
    Split markdown into blocks using double newlines (paragraph breaks).
    Avoids breaking within paragraphs, code blocks, tables, etc.
    """
    return re.split(r'\n{2,}', text.strip())

def smart_split_markdown(text, max_chunk_tokens=2000):
    lines = text.splitlines(keepends=True)
    chunks = []
    current_chunk = ""
    current_tokens = 0
    inside_code_block = False

    block = []

    def flush_block():
        nonlocal current_chunk, current_tokens, block, chunks
        block_text = ''.join(block)
        block_tokens = estimate_token_count(block_text)
        if current_tokens + block_tokens > max_chunk_tokens and not inside_code_block:
            if current_chunk.strip():
                chunks.append(current_chunk.rstrip())
            current_chunk = block_text
            current_tokens = block_tokens
        else:
            current_chunk += block_text
            current_tokens += block_tokens
        block = []

    for line in lines:
        stripped = line.strip()

        # Toggle fenced code block state
        if re.match(r'^(```|~~~)', stripped):
            inside_code_block = not inside_code_block

        # Start of a new block (blank line separates blocks)
        if not stripped and not inside_code_block:
            block.append(line)
            flush_block()
        else:
            block.append(line)

    # Flush final block
    if block:
        flush_block()
    if current_chunk.strip():
        chunks.append(current_chunk.rstrip())

    return chunks

def translate_text(text, target_language):

    print(f"Translating to {lang_dict[target_language]} using OpenAI API...")
    total_tokens = estimate_token_count(text)
    print(f"Total tokens in text: {total_tokens}")

       # Threshold — adjust based on your comfort zone and observed success (16k is conservative)
    if total_tokens < 3000:
        print(f"File is small enough ({total_tokens} tokens). Translating in one call.")
        return translate_text_gpt(text, target_language).strip()
    

    print(f"File too large ({total_tokens} tokens). Splitting into chunks...")
    chunks = smart_split_markdown(text)
    translated_chunks = []

    for i, chunk in enumerate(chunks):
        print(f"Translating chunk {i+1}/{len(chunks)}...")
        translated = translate_text_gpt(chunk, target_language)
        translated_chunks.append(translated.strip())

    return "\n\n".join(translated_chunks)


def translate_text_gpt(text, target_language):

    

    prompt = f"""
        You are a professional translator specializing in technical Markdown documentation.

        Translate the following content **into {lang_dict[target_language]} only**. Do not use or mix in other languages.

        Ensure that:
        - All headings, code blocks, links, and formatting are preserved exactly.
        - Technical and domain-specific terms are translated with care, not literally.
        - Sentences and paragraphs remain semantically equivalent to the original English.
        - Do NOT translate or modify Markdown links or images. This means the entire expression [link text](URL) or ![alt text](URL) must be preserved exactly 
        - Do NOT translate text inside backticks (`...`), single quotes ('...'), or angle brackets (<...>) — they may represent code, UI labels, or placeholders, and must be left as-is.
        - Do NOT translate anything inside fenced code blocks (those surrounded by triple backticks like ```bash ... ``` or ```python ... ```).
        - Do **NOT** translate or alter the following specific terms: {excluded_terms}. These terms must remain exactly as they appear, including capitalization and formatting.
        - **IMPORTANT**: Do NOT wrap the translated content in any ```markdown or ``` backticks — return only the translation itself.

        Here is the Markdown content to translate:

        {text}
    """

    print(f"Translating to {lang_dict[target_language]} using OpenAI API")
    
    # Create Azure OpenAI client with azure style configuration
    from openai import AzureOpenAI
    
    client = AzureOpenAI(
        api_key=OPENAI_API_KEY,
        api_version="2023-05-15",  # Use the appropriate API version
        azure_endpoint=openai.api_base
    )
    
    response = client.chat.completions.create(
        model="WIS2-MoC-gpt-4o",  # This should match your deployment name in Azure the other one is WIS2-MoC-gpt-4o
        messages=[
            {"role": "system", "content": "You are an expert Markdown translator with domain-specific knowledge."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4096,
        temperature=0.2
    )
    
    print("Finish reason:", response.choices[0].finish_reason)
    if response.choices[0].finish_reason == 'length':
        print("Warning: response was truncated due to max tokens.")
        # raise Exception and stop the script
        raise Exception("Response was truncated due to max tokens.")
    
    return response.choices[0].message.content


def translate_file(source_path: Path, lang: str):
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"Translating {source_path} to {lang}")
    total_tokens = estimate_token_count(content)
    print(f"Total tokens in file: {total_tokens}")
  
    # if total_tokens < 3000:
    #     print(f"skipping file {source_path} as it is small enough ({total_tokens} tokens).")
    #     return
    translated = translate_text(content, lang)

        
    dest_path = BASE_DIR / lang / source_path.relative_to(EN_DIR)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(translated)
    print(f"Translated {source_path} → {dest_path}")


def main():
    if '--changed-only' in sys.argv:
        changed = get_changed_files()
        md_files = [Path(f) for f in changed if f.startswith(str(EN_DIR))]
    else:
        # translate all files in the EN_DIR
        md_files = list(EN_DIR.rglob('csv2bufr-templates.md'))
    
    print(f"target languages: {TARGET_LANGS}")
    print(f"Found {len(md_files)} Markdown files to translate.")
    # print filse names/paths
    for md_file in md_files:
        print(md_file)
    if not md_files:
        print("No Markdown files found.")
        return
    
    for md_file in md_files:
        for lang in TARGET_LANGS:
            translate_file(md_file, lang)


if __name__ == '__main__':
    main()
