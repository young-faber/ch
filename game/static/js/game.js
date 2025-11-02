// Находим контейнер доски <div id="board"></div>
const board = document.getElementById("board");

// Здесь будем хранить индекс выбранной клетки (0..63).
// Если ничего не выбрано — null.
let selectedCell = null;

/**
 * Перерисовывает шахматную доску.
 * @param {string[][]} boardData - матрица 8x8; в ячейке либо пусто (null/""), либо символ фигуры.
 */
function renderBoard(boardData) {
    // Каждый раз начинаем с пустого контейнера
    board.innerHTML = '';
    
    // Два вложенных цикла создают 64 клетки
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            // Создаём DOM-элемент клетки
            const cell = document.createElement("div");
            cell.classList.add("cell");

            // Чередуем цвет: сумма чётная — светлая, нечётная — тёмная
            cell.classList.add((row + col) % 2 === 0 ? "light" : "dark");

            // Достаём фигуру из данных и, если есть, кладём в клетку
            const piece = boardData[row][col];
            if (piece) {
                cell.textContent = piece;
            }

            // В идеале полезно сохранить координаты прямо в атрибутах,
            // чтобы потом не вычислять их через индекс:
            // cell.dataset.row = row;
            // cell.dataset.col = col;

            // Добавляем клетку на доску
            board.appendChild(cell);
        }
    }
}

// Один обработчик на весь контейнер — используем делегирование событий
board.addEventListener('click', (e) => {
    // Нас интересуют только клики по .cell; если кликнули мимо — выходим
    const clickedCell = e.target.closest('.cell');
    if (!clickedCell || !board.contains(clickedCell)) return;

    // Собираем список клеток в линейный массив, чтобы получить индекс нажатой
    const cells = Array.from(document.querySelectorAll('.cell'));
    const index = cells.indexOf(clickedCell);

    // Пересчитываем индекс в координаты (row, col)
    const row = Math.floor(index / 8);
    const col = index % 8;

    // ВЕТКА 1: клик по подсвеченной клетке возможного хода
    if (clickedCell.classList.contains('possible-move')) {
        // Координаты исходной клетки берём из selectedCell
        const fromRow = Math.floor(selectedCell / 8);
        const fromCol = selectedCell % 8;
        

        // Шлём ход на сервер. Сервер отвечает JSON: { success: true/false, ... }
        let gameId = localStorage.getItem('game_id');
        fetch(`/game/move_figure/${gameId}/?from_row=${fromRow}&from_col=${fromCol}&to_row=${row}&to_col=${col}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Если ход принят, перетягиваем актуальную позицию и перерисовываем
                    console.log("Move successful");
                    let gameId = localStorage.getItem('game_id');
                    fetch('/game/get_board/' + gameId)
                        .then(response => response.json())
                        .then(data => renderBoard(data.board));
                }
                // В любом случае убираем подсветку возможных ходов
                document.querySelectorAll('.possible-move')
                    .forEach(cell => cell.classList.remove('possible-move'));
            })
            .catch(err => {
                console.error("Move error:", err);
                // На вкус можно ещё и подсветку убрать, чтобы не висела
                document.querySelectorAll('.possible-move')
                    .forEach(cell => cell.classList.remove('possible-move'));
            });

    // ВЕТКА 2: обычный клик по клетке — выбираем фигуру и подсвечиваем ходы
    } else {
        // Запоминаем выбранную клетку (её линейный индекс 0..63)
        selectedCell = index;
        
        // Сначала снимаем старую подсветку
        document.querySelectorAll('.possible-move')
            .forEach(cell => cell.classList.remove('possible-move'));

        // Просим сервер вернуть список ходов из клетки (row, col).
        // Ожидаемый ответ: { moves: [[r1,c1], [r2,c2], ...] }
        let game_id = localStorage.getItem('game_id');
        fetch(`/game/get_moves/` + gameId + `/?row=${row}&col=${col}`) //как-то так я попытался сделать
        // fetch(`/game/get_moves?row=${row}&col=${col}`)
            .then(response => response.json())
            .then(data => {
                data.moves.forEach(move => {
                    const [moveRow, moveCol] = move;
                    const moveIndex = moveRow * 8 + moveCol; // переводим координаты в линейный индекс
                    cells[moveIndex].classList.add('possible-move'); // подсветка клетки как допустимого хода
                });
            })
            .catch(err => {
                console.error("Get moves error:", err);
            });
    }
});

// При загрузке страницы поднимаем текущую позицию с сервера и рисуем её
let gameId = localStorage.getItem('game_id');
fetch('/game/get_board/' + gameId)
    .then(response => response.json())
    .then(data => renderBoard(data.board))
    .catch(error => console.error("Board loading error:", error));