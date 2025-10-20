const board = document.getElementById("board");
let selectedCell = null;

function renderBoard(boardData) {
    board.innerHTML = '';
    
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            cell.classList.add((row + col) % 2 === 0 ? "light" : "dark");
            
            const piece = boardData[row][col];
            if (piece) {
                cell.textContent = piece;
            }
            
            board.appendChild(cell);
        }
    }
}

board.addEventListener('click', (e) => {
    const clickedCell = e.target;
    const cells = Array.from(document.querySelectorAll('.cell'));
    const index = cells.indexOf(clickedCell);
    const row = Math.floor(index / 8);
    const col = index % 8;

    if (clickedCell.classList.contains('possible-move')) {
        const fromRow = Math.floor(selectedCell / 8);
        const fromCol = selectedCell % 8;
        
        fetch(`/game/move_figure?from_row=${fromRow}&from_col=${fromCol}&to_row=${row}&to_col=${col}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    fetch('/game/get_board')
                        .then(response => response.json())
                        .then(data => renderBoard(data.board));
                }
                document.querySelectorAll('.possible-move')
                    .forEach(cell => cell.classList.remove('possible-move'));
            });
    } else {
        selectedCell = index;
        
        document.querySelectorAll('.possible-move')
            .forEach(cell => cell.classList.remove('possible-move'));

        fetch(`/game/get_moves?row=${row}&col=${col}`)
            .then(response => response.json())
            .then(data => {
                data.moves.forEach(move => {
                    const [moveRow, moveCol] = move;
                    const moveIndex = moveRow * 8 + moveCol;
                    cells[moveIndex].classList.add('possible-move');
                });
            });
    }
});

// Initial board render
fetch('/game/get_board')
    .then(response => response.json())
    .then(data => renderBoard(data.board))
    .catch(error => console.error("Board loading error:", error));