import re
import fitz  # PyMuPDF

def is_reduplicated(word):
    # Check for repeated 2 or 3 letter substrings followed by S or another character
    for length in [2, 3]:
        part = word[:length]
        if word == part * 2 + 'S' or word == part * 2 + part:
            return True
    return False

def extract_words_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_words = set()
    pattern = re.compile(r'\b[A-Z]{7}\b')

    for page in doc:
        text = page.get_text()
        words = pattern.findall(text)
        for word in words:
            if is_reduplicated(word):
                all_words.add(word)
    
    return sorted(all_words)

# Example usage with sample file
if __name__ == "__main__":
    pdf_file = "sevens.pdf"
    matching_words = extract_words_from_pdf(pdf_file)
    with open("reduplicated_words.txt", "w") as f:
        for word in matching_words:
            f.write(word + "\n")
    print(f"Found {len(matching_words)} matching words.")
