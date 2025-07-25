import os
import re
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import openai
import tiktoken
from openai import AzureOpenAI

# ========== Configuration ==========
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EN_DIR = Path('docs/en')
BASE_DIR = Path('docs')
TARGET_LANGS = ['ar']

LANG_DICT = {
    "ar": "Arabic",
    # "fr": "French",
    # "es": "Spanish",
    # "zh": "Chinese",
    # "ru": "Russian",
}

EXCLUDED_TERMS = [
    "wis2box", "WIS2 in a box", "Global Broker", "Global Cache",
    "Global Discovery Catalogue", "WCMP2", "WIS2 Node", "WIS2",
    "MQTT", "MQTT Explorer", "Google Cloud Platform",
    "Amazon Web Services", "WMO Core Metadata Profile 2", "Data Type",
    "Centre ID", "wis2box-webapp", "wis2box-management", "wis2box-api",
    "collections/stations", "processes/wis2box", "wis2box-incoming",
    "MinIO", "Grafana", "YOUR-HOST", "wiki",
]

AZURE_OPENAI_SETTINGS = {
    "api_type": "azure",
    "api_base": "https://moc-translator.openai.azure.com/",
    "api_version": "2023-05-15",
    "deployment_name": "WIS2-MoC-gpt-4o",
}

# Set global OpenAI config (legacy API compatibility)
openai.api_type = AZURE_OPENAI_SETTINGS["api_type"]
openai.api_base = AZURE_OPENAI_SETTINGS["api_base"]
openai.api_key = OPENAI_API_KEY

client = AzureOpenAI(
    api_key=OPENAI_API_KEY,
    api_version=AZURE_OPENAI_SETTINGS["api_version"],
    azure_endpoint=AZURE_OPENAI_SETTINGS["api_base"]
)

# ========== Token Utility ==========
def estimate_token_count(text, model="gpt-4-turbo"):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

# ========== File Utilities ==========
def get_changed_files():
    result = subprocess.run(
        ['git', 'diff', '--name-only', 'HEAD^..HEAD'],
        stdout=subprocess.PIPE, text=True, check=True
    )
    return [f.strip() for f in result.stdout.splitlines() if f.endswith(('.md', '.pages'))]

# ========== Markdown Splitting ==========
def smart_split_markdown(text, max_chunk_tokens=2000):
    lines = text.splitlines(keepends=True)
    chunks, current_chunk, current_tokens, inside_code = [], "", 0, False
    block = []

    def flush_block():
        nonlocal current_chunk, current_tokens, block, chunks
        block_text = ''.join(block)
        block_tokens = estimate_token_count(block_text)
        if current_tokens + block_tokens > max_chunk_tokens and not inside_code:
            if current_chunk.strip():
                chunks.append(current_chunk.rstrip())
            current_chunk, current_tokens = block_text, block_tokens
        else:
            current_chunk += block_text
            current_tokens += block_tokens
        block.clear()

    for line in lines:
        stripped = line.strip()
        if re.match(r'^(```|~~~)', stripped):
            inside_code = not inside_code
        if not stripped and not inside_code:
            block.append(line)
            flush_block()
        else:
            block.append(line)

    if block:
        flush_block()
    if current_chunk.strip():
        chunks.append(current_chunk.rstrip())
    return chunks

# ========== Translation Core ==========
def build_translation_prompt(text, lang_code):
    return f"""
You are a professional translator specializing in technical Markdown documentation.

Translate the following content **into {LANG_DICT[lang_code]} only**. Do not use or mix in other languages.

Ensure that:
- All headings, code blocks, links, and formatting are preserved exactly.
- Technical and domain-specific terms are translated with care, not literally.
- Sentences and paragraphs remain semantically equivalent to the original English.
- Do NOT translate or modify Markdown links or images. This means the entire expression [link text](URL) or ![alt text](URL) must be preserved exactly.
- Do NOT translate text inside backticks (`...`), single quotes ('...'), or angle brackets (<...>) — they may represent code, UI labels, or placeholders, and must be left as-is.
- Do NOT translate anything inside fenced code blocks (```bash ...``` or ```python ...```).
- Do **NOT** translate or alter the following specific terms: {EXCLUDED_TERMS}.
- **IMPORTANT**: Do NOT wrap the translated content in ```markdown or triple backticks — return only the translation itself.

Here is the Markdown content to translate:

{text}
"""

def translate_chunk(text, lang_code):
    prompt = build_translation_prompt(text, lang_code)
    response = client.chat.completions.create(
        model=AZURE_OPENAI_SETTINGS["deployment_name"],
        messages=[
            {"role": "system", "content": "You are an expert Markdown translator with domain-specific knowledge."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4096,
        temperature=0.2
    )
    result = response.choices[0]
    if result.finish_reason == 'length':
        raise Exception("Response was truncated due to token limits.")
    return result.message.content.strip()

def translate_text(text, lang_code):
    tokens = estimate_token_count(text)
    print(f"Total tokens: {tokens}")
    if tokens < 3000:
        return translate_chunk(text, lang_code)
    chunks = smart_split_markdown(text)
    translated = [translate_chunk(chunk, lang_code) for chunk in chunks]
    return "\n\n".join(translated)

# ========== File Translation ==========
def translate_file(source_path: Path, lang_code: str):
    normalized_path = str(source_path).replace('documentation/', '')
    source_path = Path(normalized_path)

    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Translating {source_path} → {lang_code}")
    translated = translate_text(content, lang_code)

    dest_path = BASE_DIR / lang_code / source_path.relative_to(EN_DIR)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(translated)
    print(f"✅ Saved: {dest_path}")

# ========== Main ==========
def main():
    if '--changed-only' in sys.argv:
        changed = get_changed_files()
        print(f"Changed files: {changed}")
        md_files = [
            Path(f) for f in changed
            if f.replace('documentation/', '').startswith(str(EN_DIR)) and f.endswith(('.md', '.pages'))
        ]
    else:
        md_files = list(EN_DIR.rglob('*.md')) + list(EN_DIR.rglob('*.pages'))

    if not md_files:
        print("No files to translate.")
        return

    for md_file in md_files:
        for lang in TARGET_LANGS:
            translate_file(md_file, lang)

if __name__ == '__main__':
    main()
