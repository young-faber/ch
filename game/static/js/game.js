const board = document.getElementById("board");
const userColor = localStorage.getItem("color");

function renderBoard(boardData) {
  const flipped = userColor === "black"; // чёрный смотрит снизу/сверху — как хочешь

  board.innerHTML = "";

  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const rr = flipped ? 7 - row : row;
      const cc = flipped ? 7 - col : col;

      const cell = document.createElement("div");
      cell.classList.add("cell");
      cell.classList.add((row + col) % 2 === 0 ? "light" : "dark");

      const piece = boardData[rr][cc];
      if (piece) {
        cell.textContent = piece;
      }
      board.appendChild(cell);
    }
  }
}

// function renderBoard(boardData) {
//     board.innerHTML = '';
//     for (let row = 0; row < 8; row++) {
//         for (let col = 0; col < 8; col++) {
//             const cell = document.createElement("div");
//             cell.classList.add("cell");
//             cell.classList.add((row + col) % 2 === 0 ? "light" : "dark");
//             const piece = boardData[row][col];
//             if (piece) {
//                 cell.textContent = piece;
//             }
//             board.appendChild(cell);
//         }
//     }
// }

function sendPromotionRequest(piece) {
  //get piece from button data-piece
  const gameId = localStorage.getItem("game_id");

  fetch(
    `/game/pawn_promotion/${gameId}/?piece=${piece}&row=${window.row}&col=${window.col}`
  )
    .then((r) => r.json())
    .then((data) => {
      if (!data.success) {
        alert(data.error);
        return;
      }

      // обновляем доску
      renderBoard(data.board);

      // закрываем окно
      document.getElementById("promotion-dialog").style.display = "none";
    });
}

board.addEventListener("click", (e) => {
  const clickedCell = e.target.closest(".cell");
  if (!clickedCell || !board.contains(clickedCell)) return;

  const cells = Array.from(document.querySelectorAll(".cell"));
  const index = cells.indexOf(clickedCell);
  // display coords (как на странице)
  const dispRow = Math.floor(index / 8);
  const dispCol = index % 8;

  const flipped = userColor === "black"; // true если доска перевёрнута для пользователя

  // логические координаты в boardData (то, что ожидает бэкенд)
  const row = flipped ? 7 - dispRow : dispRow;
  const col = flipped ? 7 - dispCol : dispCol;
  //if flipped, то результат после вопроса (7 - ...) иначе результат после :

  // ВЕТКА 1: клик по подсвеченной клетке возможного хода
  if (clickedCell.classList.contains("possible-move")) {
    const fromRow = Math.floor(selectedCell / 8);
    const fromCol = selectedCell % 8;

    let gameId = localStorage.getItem("game_id");
    fetch(
      `/game/move_figure/${gameId}/?from_row=${fromRow}&from_col=${fromCol}&to_row=${row}&to_col=${col}`
    )
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          if (data.message == "pawn_promotion") {
            window.row = data.to_row;
            window.col = data.to_col;

            document.getElementById("promotion-dialog").style.display = "block";
            const promotionButtons =
              document.querySelectorAll(".promotion-button");
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
        document
          .querySelectorAll(".possible-move")
          .forEach((cell) => cell.classList.remove("possible-move"));
      })
      .catch((err) => {
        console.error("Move error:", err);
        document
          .querySelectorAll(".possible-move")
          .forEach((cell) => cell.classList.remove("possible-move"));
      });
  }
  // ВЕТКА 2: обычный клик по клетке
  else {
    selectedCell = row * 8 + col;
    document
      .querySelectorAll(".possible-move")
      .forEach((cell) => cell.classList.remove("possible-move"));

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

// Initial board load
function loadBoard(gameId) {
  fetch("/game/get_board/" + gameId)
    .then((response) => response.json())
    .then((data) => renderBoard(data.board))
    .catch((error) => console.error("Board loading error:", error));
}

let game_id = localStorage.getItem("game_id");
let move_id = localStorage.getItem("move_id");
loadBoard(game_id);

fetch(`/game/long_polling/get_board/${game_id}?move_id=${move_id}`)
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
    localStorage.setItem("move_id", move_id);
    loadBoard(game_id);
  });
