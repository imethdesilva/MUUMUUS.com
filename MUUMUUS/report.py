from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def draw_scrabble_word(c, word, x, y):
    tile_size = 30
    spacing = 5

    for i, letter in enumerate(word):
        # Draw tile
        c.setFillColor(colors.beige)
        c.rect(x + i * (tile_size + spacing), y, tile_size, tile_size, fill=1, stroke=1)

        # Draw letter
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(x + i * (tile_size + spacing) + tile_size / 2, y + tile_size / 2 - 5, letter)

def create_pdf(words_and_defs, output_filename):
    c = canvas.Canvas(output_filename, pagesize=LETTER)
    width, height = LETTER
    x_margin, y_margin = 50, 720
    y = y_margin

    for word, definition in words_and_defs:
        draw_scrabble_word(c, word, x_margin, y)

        # Draw definition under it
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.darkgray)
        c.drawString(x_margin, y - 20, definition)

        y -= 80
        if y < 100:
            c.showPage()
            y = y_margin

    c.save()
    print(f"✅ PDF saved as {output_filename}")

# Example: You would replace this with your actual 50 words and defs
sample_words = [
    ("MUUMUUS", "a loose Hawaiian dress"),
    ("TOETOES", "tall grass in New Zealand"),
    ("MAOMAOS", "Chinese revolutionary soldiers"),
    ("NEINEIS", "a type of goosefish"),
    # Add more...
]

create_pdf(sample_words, "Reduplicated_Words.pdf")
