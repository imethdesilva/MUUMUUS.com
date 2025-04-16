import re
import fitz  # PyMuPDF

def is_reduplicated(word):
    for length in [2, 3]:
        part = word[:length]
        if word == part * 2 + 'S' or word == part * 2 + part:
            return True
    return False

def extract_words_and_definitions_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    results = {}
    pattern = re.compile(r'\b[A-Z]{7}\b')

    for page in doc:
        text = page.get_text()

        # Combine lines to handle wrapped definitions
        lines = text.split('\n')
        combined_text = ' '.join(lines)

        # Match format: WORD followed by space(s) and its definition
        entries = re.findall(r'(\b[A-Z]{7}\b)\s+([^[]+)', combined_text)

        for word, raw_def in entries:
            if is_reduplicated(word) and word not in results:
                # Clean definition
                cleaned_def = raw_def.strip().strip(':.;,')
                results[word] = cleaned_def

    return results

# Example usage
if __name__ == "__main__":
    pdf_file = "sevens.pdf"
    word_defs = extract_words_and_definitions_from_pdf(pdf_file)

    with open("reduplicated_words_with_defs.txt", "w", encoding="utf-8") as f:
        for word, definition in sorted(word_defs.items()):
            f.write(f'("{word}", "{definition}"),\n')

    print(f"✅ Found {len(word_defs)} reduplicated words with definitions.")
