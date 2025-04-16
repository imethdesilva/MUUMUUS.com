from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import os

# Scrabble letter values (EN version)
letter_points = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2,
    'E': 1, 'F': 4, 'G': 2, 'H': 4,
    'I': 1, 'J': 8, 'K': 5, 'L': 1,
    'M': 3, 'N': 1, 'O': 1, 'P': 3,
    'Q': 10, 'R': 1, 'S': 1, 'T': 1,
    'U': 1, 'V': 4, 'W': 4, 'X': 8,
    'Y': 4, 'Z': 10
}

# Modern Scrabble-inspired color palette
TILE_BG = HexColor('#F5E9CB')       # Light cream for tiles
TILE_BORDER = HexColor('#BA8755')    # Wood-like border
HEADER_BG = HexColor('#006C3C')      # Scrabble board green
HEADER_TEXT = HexColor('#FFFFFF')    # White text
TEXT_COLOR = HexColor('#333333')     # Dark gray for text

def draw_tile(c, letter, x, y, tile_size=24):
    """Draw a single Scrabble tile with authentic styling"""
    # Tile shadow
    c.setFillColor(HexColor('#DDDDDD'))
    c.roundRect(x+1, y-1, tile_size, tile_size, 2, fill=1, stroke=0)
    
    # Tile background
    c.setFillColor(TILE_BG)
    c.roundRect(x, y, tile_size, tile_size, 2, fill=1, stroke=0)
    
    # Tile border
    c.setStrokeColor(TILE_BORDER)
    c.setLineWidth(0.8)
    c.roundRect(x, y, tile_size, tile_size, 2, fill=0, stroke=1)
    
    # Main letter - perfectly centered
    c.setFillColor(TEXT_COLOR)
    c.setFont("Helvetica-Bold", 16)
    
    # Draw the letter exactly in the center 
    c.drawCentredString(x + tile_size/2, y + tile_size/2 - 3, letter)
    
    # Point value - bottom right corner (authentic Scrabble placement)
    points = letter_points.get(letter.upper(), 0)
    c.setFont("Helvetica", 6)
    c.setFillColor(HexColor('#444444'))
    c.drawRightString(x + tile_size - 2, y + 2, str(points))

def draw_scrabble_word(c, word, x, y, tile_size=24):
    """Draw a word using Scrabble tiles with authentic styling"""
    spacing = 2  # Space between tiles
    
    for i, letter in enumerate(word):
        tile_x = x + i * (tile_size + spacing)
        draw_tile(c, letter, tile_x, y, tile_size)
    
    # Return the total width
    return len(word) * (tile_size + spacing) - spacing

def create_pdf(words, output_filename):
    c = canvas.Canvas(output_filename, pagesize=LETTER)
    page_width, page_height = LETTER
    
    words_per_page = 30
    words_per_column = 15
    
    # Calculate how many pages we need
    total_words = len(words)
    total_pages = (total_words + words_per_page - 1) // words_per_page

    # Calculate column positions (keep track of column centers)
    col1_center = left_margin + (col_width / 2)
    col2_center = center_x + 15 + (col_width / 2)
    
    for page in range(total_pages):
        # Draw header on each page
        header_height = 50
        c.setFillColor(HEADER_BG)
        c.rect(0, page_height - header_height, page_width, header_height, fill=1, stroke=0)
        
        # Header text
        c.setFillColor(HEADER_TEXT)
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(page_width/2, page_height - 35, "REDUPLICATED SEVENS")
        
        # Calculate available space - increased space below header
        top_margin = 785 - 70  # More space below header
        bottom_margin = 30     # Space at bottom
        available_height = top_margin - bottom_margin
        
        # Calculate row height based on available space
        row_height = available_height / words_per_column
        
        # Setup margins and spacing
        left_margin = 30
        right_margin = page_width - 30
        
        # Calculate column width
        col_width = (right_margin - left_margin - 30) / 2  # 30 is gutter width
        
        # Calculate tile size based on available space
        # For 7-letter words with spacing
        tile_size = 24  # Fixed tile size for better appearance
        
        # Draw subtle column divider
        center_x = page_width / 2
        c.setStrokeColor(HexColor('#DDDDDD'))
        c.setDash([2, 3], 0)
        c.line(center_x, top_margin + 5, center_x, bottom_margin - 5)
        c.setDash([], 0)
        
        # Calculate column positions
        col1_x = left_margin
        col2_x = center_x + 15
        
        # Draw words for this page
        for col in range(2):  # Two columns
            for row in range(words_per_column):
                word_idx = page * words_per_page + col * words_per_column + row
                
                if word_idx < len(words):
                    word = words[word_idx]
                    
                    # Get column center position
                    column_center = col1_center if col == 0 else col2_center
                    
                    # Calculate total word width
                    word_width = (len(word) * (tile_size + spacing)) - spacing
                    
                    # Calculate x position to center the word in the column
                    x = column_center - (word_width / 2)
                    
                    # Y position: calculate position to evenly distribute
                    y = top_margin - (row * row_height) - 15
                    
                    # Draw word
                    draw_scrabble_word(c, word, x, y, tile_size)

       # Add page number at bottom (except for single page documents)
        if total_pages > 1:
            c.setFont("Helvetica", 8)
            c.setFillColor(TEXT_COLOR)
            c.drawCentredString(page_width/2, 20, f"Page {page+1} of {total_pages}")
            
        # Add attribution
        c.setFont("Helvetica", 6)
        c.setFillColor(HexColor('#888888'))
        c.drawCentredString(page_width/2, 12, "Scrabble Word Reference • Reduplicated Seven-Letter Words • Meith ")
            
        if page < total_pages - 1:
            c.showPage()  # New page
            
    
    c.save()
    print(f"✅ Optimized Scrabble-style PDF saved as: {output_filename}")
    
    # Print the full path to the saved file
    abs_path = os.path.abspath(output_filename)
    print(f"File saved at: {abs_path}")

# Word list - just the words without definitions
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

create_pdf(reduplicated_words, "Reduplicated_Sevens_Optimized.pdf")