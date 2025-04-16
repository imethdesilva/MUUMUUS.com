from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import os
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT

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
HEADER_BG = HexColor('#6C0BA9')      # Scrabble board green
HEADER_TEXT = HexColor('#FFFFFF')    # White text
TEXT_COLOR = HexColor('#333333')     # Dark gray for text
BOX_COLOR = HexColor('#E0E0E0')      # Light gray for boxes
BOX_BORDER = HexColor('#AAAAAA')     # Medium gray for box borders

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

def draw_definition_box(c, definition, x, y, width, height=50):
    """Draw a word definition with proper wrapping in a box"""
    # Draw background box for definition
    c.setFillColor(BOX_COLOR)
    c.setStrokeColor(BOX_BORDER)
    c.setLineWidth(0.5)
    c.roundRect(x, y - height, width, height, 5, fill=1, stroke=1)
    
    # Create paragraph style
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(
        'Definition',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=TEXT_COLOR,
        leading=12,  # Line spacing
        alignment=TA_LEFT,
        allowWidows=0,
        allowOrphans=0
    )
    
    # Create paragraph object with appropriate padding
    padding = 10
    p = Paragraph(definition, custom_style)
    
    # Make sure text fits within the box with padding
    available_width = width - (2 * padding)
    available_height = height - (2 * padding)
    
    # Get width and height of the paragraph
    w, h = p.wrap(available_width, available_height)
    
    # Draw the paragraph inside the box with padding
    p.drawOn(c, x + padding, y - height + padding)
    
    return height

def create_pdf(words, definitions, output_filename):
    c = canvas.Canvas(output_filename, pagesize=LETTER)
    page_width, page_height = LETTER
    
    words_per_page = 13
    
    # Calculate how many pages we need
    total_words = len(words)
    total_pages = (total_words + words_per_page - 1) // words_per_page
    
    for page in range(total_pages):
        # Draw header on each page
        header_height = 50
        c.setFillColor(HEADER_BG)
        c.rect(0, page_height - header_height, page_width, header_height, fill=1, stroke=0)
        
        # Header text
        c.setFillColor(HEADER_TEXT)
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(page_width/2, page_height - 35, "REDUPLICATED SEVENS")
        
        # Setup margins and spacing
        left_margin = 30
        right_margin = page_width - 30
        
        # Calculate column width and positions
        center_x = page_width / 2
        col_width = (right_margin - left_margin - 30) / 2  # 30 is gutter width
        
        # Calculate available space - increased space below header
        top_margin = 785 - 70  # More space below header
        bottom_margin = 30     # Space at bottom
        available_height = top_margin - bottom_margin
        
        # Calculate row height based on available space
        row_height = available_height / words_per_page
        
        # Calculate tile size based on available space
        tile_size = 28  # Fixed tile size for better appearance
        spacing = 2     # Space between tiles
        
        # Draw words and definitions for this page
        for row in range(words_per_page):
            word_idx = page * words_per_page + row
            
            if word_idx < len(words):
                word = words[word_idx]
                definition = definitions[word_idx]
                
                # Calculate positions
                # Words on the left side
                word_x = left_margin + 20  # Left align the words, with some padding
                
                # Definitions on the right side
                def_x = center_x + 15  # Start definitions after center line with padding
                def_width = col_width - 25  # Leave some margin, reduced to ensure text fits
                
                # Y position: calculate position to evenly distribute
                y = top_margin - (row * row_height) - 35
                
                # Draw word (no box, just the tiles)
                draw_scrabble_word(c, word, word_x, y, tile_size)
                
                # Fixed height for definition box
                def_box_height = 36  # Adjusted for better appearance
                
                # Draw definition in a box
                draw_definition_box(c, definition, def_x, y + 30, def_width, def_box_height)

        # Add page number at bottom
        if total_pages > 1:
            c.setFont("Helvetica", 8)
            c.setFillColor(TEXT_COLOR)
           
            
        # Add attribution
        c.setFont("Helvetica", 8)
        c.setFillColor(HexColor('#888888'))
        c.drawCentredString(page_width/2, 14, "Scrabble • Reduplicated Seven-Letter Words • Compiled by Meith ")
            
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

# Create dummy definitions - one for each word
definitions = [
    "New Zealand tree [n]",
    "TREVALLY, any of various food and game fishes [n]",
    "Grazing marine gastropod [n]",
    "Native American throwing stick [n]",
    "Air rifle [n]",
    "berbere (hot-tasting Ethiopian paste)",  
    "Sweet [n]",
    "Blunder [n]",
    "Long flowing garment [n]",
    "Black robe worn by Muslim women in East Africa [n]",
    "Songbird of tropical Africa and Asia [n]",
    "Lively high-kicking dance performed by a female group [n]",
    "Affectedly pretty or stylish [adj]",
    "Chayote (tropical climbing plant) [n]", 
    "Small African antelope [n]",
    "Excrement (slang) [n]",
    "Soft-nosed bullet [n]",
    "Scurf or scaling of the skin [n]",
    "African talisman, amulet, or charm [n]",
    "Tropical American palm [n]",
    "Indian cotton cloth [n]",
    "Not Family [v]",  
    "Food [n]",
    "Climbing bush plant of New Zealand [n]",
    "Red pigment used by Hindu women to make a mark on the forehead [n]",
    "Twining leguminous plant [n]",
    "Logarithm of a logarithm (in equations, etc) [n]",
    "Fish of New Zealand seas [n]",
    "Tropical American bird with a long tail and blue and brownish-green plumage [n]",
    "Muslin [n]",
    "Speak or say in a quiet indistinct way [v]",
    "Loose brightly coloured dress worn by women in Hawaii [n]",
    "Type of plant [n]",
    "pawpaw",  
    "New Zealand thrush, thought to be extinct [n]",
    "Skirt worn by Maoris on ceremonial occasions [n]",
    "Decorative ball of tufted wool, silk, etc [n]",
    "Sansar (name of a wind that blows in Iran)",  
    "Sesame [n]",
    "Arctic ground squirrel [n]",
    "Hard deposit on the teeth [n]",
    "toitoi (tall grasses with feathery fronds)",  
    "Tall grasses with feathery fronds [n]",
    "Any of various bloodsucking African flies [n]",
    "tsk (utter the sound 'tsk', usu in disapproval) [v]",  
    "Edible marine bivalve of New Zealand waters [n]",
    "TSETSE, any of various bloodsucking African flies [n]", 
    "Tassels or fringes of thread attached to the four corners of tallith [n]",
    "Urinate [v]",
    "Wood pigeon [n]"
]


create_pdf(reduplicated_words, definitions, "Reduplicated_Sevens_Fixed.pdf")