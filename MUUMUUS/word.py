import fitz  # PyMuPDF
import re

# List of target words
reduplicated_words = [
    "AKEAKES", "ARAARAS", "ATAATAS", "ATLATLS", "BEEBEES",
    "BERBERS", "BONBONS", "BOOBOOS", "BOUBOUS", "BUIBUIS",
    "BULBULS", "CANCANS", "CHICHIS", "CHOCHOS", "DIKDIKS",
    "DOODOOS", "DUMDUMS", "FURFURS", "GRIGRIS", "GRUGRUS",
    "HUMHUMS", "JIGJIGS", "KAIKAIS", "KIEKIES", "KUMKUMS",
    "LABLABS", "LOGLOGS", "MAOMAOS", "MOTMOTS", "MULMULS",
    "MURMURS", "MUUMUUS", "NEINEIS", "PAWPAWS", "PIOPIOS",
    "PIUPIUS", "POMPOMS", "SARSARS", "SEMSEMS", "SIKSIKS",
    "TARTARS", "TOETOES", "TOITOIS", "TSETSES", "TSKTSKS",
    "TUATUAS", "TZETZES", "TZITZIS", "WEEWEES", "ZOOZOOS"
]

# Store found definitions
found_definitions = {}

# Open the PDF file
pdf_path = "sevens.pdf"  # Replace with the actual file name
doc = fitz.open(pdf_path)

# Compile a regex to match definitions following the word
def_pattern = re.compile(rf"\b({'|'.join(reduplicated_words)})\b[^\n]*\n([^\n]+)")

# Iterate through pages
for page_num in range(len(doc)):
    text = doc.load_page(page_num).get_text()
    for match in def_pattern.finditer(text):
        word, definition = match.groups()
        if word not in found_definitions:  # Only take the first definition found
            found_definitions[word] = definition.strip()

# Write definitions to a text file in the order of reduplicated_words
with open("definitions.txt", "w", encoding="utf-8") as f:
    for word in reduplicated_words:
        definition = found_definitions.get(word, "Definition not found.")
        f.write(f'"{definition}",\n')

print("✅ Definitions have been written to 'definitions.txt'")
