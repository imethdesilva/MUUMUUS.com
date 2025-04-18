// Scrabble tile distribution and values
const tileBag = [
    { letter: 'E', value: 1, count: 12 },
    { letter: 'A', value: 1, count: 9 },
    { letter: 'I', value: 1, count: 9 },
    { letter: 'O', value: 1, count: 8 },
    { letter: 'N', value: 1, count: 6 },
    { letter: 'R', value: 1, count: 6 },
    { letter: 'T', value: 1, count: 6 },
    { letter: 'L', value: 1, count: 4 },
    { letter: 'S', value: 1, count: 4 },
    { letter: 'U', value: 1, count: 4 },
    { letter: 'D', value: 2, count: 4 },
    { letter: 'G', value: 2, count: 3 },
    { letter: 'B', value: 3, count: 2 },
    { letter: 'C', value: 3, count: 2 },
    { letter: 'M', value: 3, count: 2 },
    { letter: 'P', value: 3, count: 2 },
    { letter: 'F', value: 4, count: 2 },
    { letter: 'H', value: 4, count: 2 },
    { letter: 'V', value: 4, count: 2 },
    { letter: 'W', value: 4, count: 2 },
    { letter: 'Y', value: 4, count: 2 },
    { letter: 'K', value: 5, count: 1 },
    { letter: 'J', value: 8, count: 1 },
    { letter: 'X', value: 8, count: 1 },
    { letter: 'Q', value: 10, count: 1 },
    { letter: 'Z', value: 10, count: 1 },
    { letter: '?', value: 0, count: 2 } // Blank tiles
];

// Create a full tile bag based on the distribution
let fullTileBag = [];
tileBag.forEach(tile => {
    for (let i = 0; i < tile.count; i++) {
        fullTileBag.push({ letter: tile.letter, value: tile.value });
    }
});

// Shuffle the tile bag to get random tiles
function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// Function to generate a random tile rack of 7 tiles
function generateTileRack() {
    shuffle(fullTileBag);
    return fullTileBag.slice(0, 7);
}

// Function to display the tile rack in the UI
function displayTileRack() {
    const tileRackDiv = document.getElementById('tile-rack');
    tileRackDiv.innerHTML = ''; // Clear existing tiles

    const tileRack = generateTileRack();
    
    tileRack.forEach(tile => {
        const tileDiv = document.createElement('div');
        tileDiv.classList.add('tile');
        tileDiv.textContent = tile.letter;

        const tileValueDiv = document.createElement('div');
        tileValueDiv.classList.add('tile-value');
        tileValueDiv.textContent = tile.value;

        // Enable drag events
        tileDiv.setAttribute('draggable', true);
        tileDiv.addEventListener('dragstart', dragStart);
        tileDiv.addEventListener('dragend', dragEnd);

        tileDiv.appendChild(tileValueDiv);
        tileRackDiv.appendChild(tileDiv);
    });
}

// Drag and drop functionality
let draggingTile = null;

// Function to handle drag start
function dragStart(e) {
    draggingTile = this;
    this.classList.add('dragging'); // Add a class to style the dragging tile
}

// Function to handle drag end
function dragEnd() {
    this.classList.remove('dragging'); // Remove the class when dragging ends
}

// Allow dropping on tile rack
const tileRackDiv = document.getElementById('tile-rack');
tileRackDiv.addEventListener('dragover', e => {
    e.preventDefault(); // Allow drop
});

tileRackDiv.addEventListener('drop', e => {
    e.preventDefault();
    if (draggingTile) {
        // Find the position of the dragging tile
        const tiles = Array.from(tileRackDiv.children);
        const draggingIndex = tiles.indexOf(draggingTile);
        const dropIndex = tiles.length;

        // Move the dragging tile to the new position
        tileRackDiv.insertBefore(draggingTile, tiles[dropIndex]);

        // If dropping before another tile, adjust accordingly
        const targetTile = e.target.closest('.tile');
        if (targetTile && targetTile !== draggingTile) {
            tileRackDiv.insertBefore(draggingTile, targetTile);
        }

        draggingTile = null; // Reset draggingTile
    }
});

// Toggle dark mode
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const darkModeBtn = document.getElementById('dark-mode-btn');
    
    // Change button text based on current mode
    if (document.body.classList.contains('dark-mode')) {
        darkModeBtn.textContent = 'Switch to Light Mode'; // Change text when dark mode is active
    } else {
        darkModeBtn.textContent = 'Switch to Dark Mode'; // Change text when dark mode is inactive
    }
}

// Set up the button to toggle dark mode on click
document.getElementById('dark-mode-btn').addEventListener('click', toggleDarkMode);

// Set up the button to generate a new rack on click
document.getElementById('generate-btn').addEventListener('click', displayTileRack);

// Generate the first rack on page load
displayTileRack();