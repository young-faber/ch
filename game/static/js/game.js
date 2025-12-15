const board = document.getElementById("board");
const userColor = localStorage.getItem("color");
let selectedCell = null;

function getPieceInfo(piece) {
  if (!piece) return null;

  const letterMap = {
    'K': 'king',
    'Q': 'queen',
    'R': 'rook',
    'B': 'bishop',
    'N': 'knight',
    'P': 'pawn',
  };

  // Новая логика: если формат "Kw", "Qb" и т.д.
  if (typeof piece === 'string' && piece.length === 2) {
    const pieceType = piece[0]; // 'K', 'Q', 'R' и т.д.
    const color = piece[1]; // 'w' или 'b'
    
    if (letterMap[pieceType]) {
      return {
        prefix: color, // 'w' или 'b'
        type: letterMap[pieceType] // 'king', 'queen' и т.д.
      };
    }
  }

  // Старая логика для буквы (одиночный символ)
  if (typeof piece === 'string' && piece.length === 1) {
    const upper = piece.toUpperCase();
    if (letterMap[upper]) {
      const type = letterMap[upper];
      const prefix = piece === upper ? 'w' : 'b';
      return { prefix, type };
    }
  }

  // Юникод
  const unicodeMap = {
    '♔': ['w','king'], '♕': ['w','queen'], '♖': ['w','rook'],
    '♗': ['w','bishop'], '♘': ['w','knight'], '♙': ['w','pawn'],
    '♚': ['b','king'], '♛': ['b','queen'], '♜': ['b','rook'],
    '♝': ['b','bishop'], '♞': ['b','knight'], '♟': ['b','pawn']
  };
  
  if (unicodeMap[piece]) {
    return { prefix: unicodeMap[piece][0], type: unicodeMap[piece][1] };
  }

  // Объект {color:'w', type:'rook'}
  if (typeof piece === 'object' && piece.color && piece.type) {
    return { prefix: piece.color, type: piece.type };
  }

  return null;
}

function getImageForPiece(piece) {
  const info = getPieceInfo(piece);
  if (!info) return null;
  return `/static/images/${info.prefix}_${info.type}.png`;
}

function renderBoard(boardData) {
  const flipped = userColor === "black";
  board.innerHTML = "";

  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const rr = flipped ? 7 - row : row;
      const cc = flipped ? 7 - col : col;

      const cell = document.createElement("div");
      cell.classList.add("cell");
      cell.classList.add((row + col) % 2 === 0 ? "light" : "dark");

      const piece = boardData[rr][cc];
      console.log(`[${rr},${cc}] piece=${piece}`);

      if (piece) {
        const imgSrc = getImageForPiece(piece);
        console.log(`  imgSrc=${imgSrc}`);

        if (imgSrc) {
          const img = document.createElement("img");
          img.src = imgSrc;
          img.alt = piece;
          img.classList.add("piece");
          img.draggable = false;
          cell.appendChild(img);
        } else {
          cell.textContent = piece;
        }
      }

      board.appendChild(cell);
    }
  }
}

function sendPromotionRequest(piece) {
  const gameId = localStorage.getItem("game_id");
  fetch(`/game/pawn_promotion/${gameId}/?piece=${piece}&row=${window.row}&col=${window.col}`)
    .then((r) => r.json())
    .then((data) => {
      if (!data.success) {
        alert(data.error);
        return;
      }
      renderBoard(data.board);
      document.getElementById("promotion-dialog").style.display = "none";
    });
}

board.addEventListener("click", (e) => {
  const clickedCell = e.target.closest(".cell");
  if (!clickedCell || !board.contains(clickedCell)) return;

  const cells = Array.from(document.querySelectorAll(".cell"));
  const index = cells.indexOf(clickedCell);
  const dispRow = Math.floor(index / 8);
  const dispCol = index % 8;

  const flipped = userColor === "black";
  const row = flipped ? 7 - dispRow : dispRow;
  const col = flipped ? 7 - dispCol : dispCol;

  // ВЕТКА 1: клик по подсвеченной клетке возможного хода
  if (clickedCell.classList.contains("possible-move")) {
    const fromRow = Math.floor(selectedCell / 8);
    const fromCol = selectedCell % 8;

    let gameId = localStorage.getItem("game_id");
    fetch(`/game/move_figure/${gameId}/?from_row=${fromRow}&from_col=${fromCol}&to_row=${row}&to_col=${col}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          if (data.message == "pawn_promotion") {
            window.row = data.to_row;
            window.col = data.to_col;
            document.getElementById("promotion-dialog").style.display = "block";
            const promotionButtons = document.querySelectorAll(".promotion-button");
            promotionButtons.forEach((button) => {
              button.onclick = () => {
                const piece = button.getAttribute("data-piece");
                sendPromotionRequest(piece);
              };
            });
            console.log("Pawn promotion triggered");
          }
          return fetch("/game/get_board/" + gameId);
        } else {
          alert(data.error);
          throw new Error(data.error);
        }
      })
      .then((response) => response.json())
      .then((data) => {
        renderBoard(data.board);
        document.querySelectorAll(".possible-move").forEach((cell) => cell.classList.remove("possible-move"));
        selectedCell = null;
      })
      .catch((err) => {
        console.error("Move error:", err);
        document.querySelectorAll(".possible-move").forEach((cell) => cell.classList.remove("possible-move"));
      });
  }
  // ВЕТКА 2: обычный клик по клетке
  else {
    selectedCell = row * 8 + col;
    document.querySelectorAll(".possible-move").forEach((cell) => cell.classList.remove("possible-move"));

    let gameId = localStorage.getItem("game_id");
    fetch(`/game/get_moves/${gameId}/?row=${row}&col=${col}`)
      .then((response) => response.json())
      .then((data) => {
        data.moves.forEach((move) => {
          const [moveRow, moveCol] = move;
          const dispMoveRow = flipped ? 7 - moveRow : moveRow;
          const dispMoveCol = flipped ? 7 - moveCol : moveCol;
          const moveIndex = dispMoveRow * 8 + dispMoveCol;
          cells[moveIndex].classList.add("possible-move");
        });
      })
      .catch((err) => console.error("Get moves error:", err));
  }
});

function loadBoard(gameId) {
  fetch("/game/get_board/" + gameId)
    .then((response) => response.json())
    .then((data) => renderBoard(data.board))
    .catch((error) => console.error("Board loading error:", error));
}

function pollForUpdates() {
  let move_id = localStorage.getItem("move_id");
  let game_id = localStorage.getItem("game_id");

  fetch(`/game/long_polling/get_board/${game_id}?move_id=${move_id}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data.move_id === null) return;
      localStorage.setItem("move_id", data.move_id);
      loadBoard(game_id);
    })
    .finally(() => {
      setTimeout(pollForUpdates, 200);
    });
}

document.addEventListener("DOMContentLoaded", () => {
  let game_id = localStorage.getItem("game_id");
  loadBoard(game_id);
  pollForUpdates();
});