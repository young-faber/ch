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
    const clickedCell = e.target.closest('.cell');
    if (!clickedCell || !board.contains(clickedCell)) return;

    const cells = Array.from(document.querySelectorAll('.cell'));
    const index = cells.indexOf(clickedCell);
    const row = Math.floor(index / 8);
    const col = index % 8;

    // ВЕТКА 1: клик по подсвеченной клетке возможного хода
    if (clickedCell.classList.contains('possible-move')) {
        const fromRow = Math.floor(selectedCell / 8);
        const fromCol = selectedCell % 8;
        
        let gameId = localStorage.getItem('game_id');
        fetch(`/game/move_figure/${gameId}/?from_row=${fromRow}&from_col=${fromCol}&to_row=${row}&to_col=${col}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    return fetch('/game/get_board/' + gameId);
                } else {
                    alert(data.error);
                    throw new Error(data.error);
                }
            })
            .then(response => response.json())
            .then(data => {
                renderBoard(data.board);
                document.querySelectorAll('.possible-move')
                    .forEach(cell => cell.classList.remove('possible-move'));
            })
            .catch(err => {
                console.error("Move error:", err);
                document.querySelectorAll('.possible-move')
                    .forEach(cell => cell.classList.remove('possible-move'));
            });
    } 
    // ВЕТКА 2: обычный клик по клетке
    else {
        selectedCell = index;
        
        document.querySelectorAll('.possible-move')
            .forEach(cell => cell.classList.remove('possible-move'));

        let gameId = localStorage.getItem('game_id');
        fetch(`/game/get_moves/${gameId}/?row=${row}&col=${col}`)
            .then(response => response.json())
            .then(data => {
                data.moves.forEach(move => {
                    const [moveRow, moveCol] = move;
                    const moveIndex = moveRow * 8 + moveCol;
                    cells[moveIndex].classList.add('possible-move');
                });
            })
            .catch(err => console.error("Get moves error:", err));
    }
});

// Initial board load
let gameId = localStorage.getItem('game_id');
fetch('/game/get_board/' + gameId)
    .then(response => response.json())
    .then(data => renderBoard(data.board))
    .catch(error => console.error("Board loading error:", error));