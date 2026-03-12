// Окно подтверждения сдачи
const surrenderBtn = document.getElementById('surrenderBtn');
const surrenderModal = document.getElementById('surrenderModal');
const confirmSurrenderBtn = document.getElementById('confirmSurrender');
const cancelSurrenderBtn = document.getElementById('cancelSurrender');

// Открыть модальное окно при нажатии кнопки "Сдаться"
surrenderBtn.addEventListener('click', () => {
  surrenderModal.classList.add('active');
});

// Закрыть модальное окно при нажатии "Отмена"
cancelSurrenderBtn.addEventListener('click', () => {
  surrenderModal.classList.remove('active');
});

// Закрыть модальное окно при клике вне его содержимого
surrenderModal.addEventListener('click', (e) => {
  if (e.target === surrenderModal) {
    surrenderModal.classList.remove('active');
  }
});

// Подтвердить сдачу и отправить на сервер
confirmSurrenderBtn.addEventListener('click', async () => {
  const gameId = localStorage.getItem('game_id');
  
  try {
    // Отправляем POST запрос на сервер
    const response = await fetch(`/game/surrender/${gameId}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        surrendered: true
      })
    });

    const data = await response.json();
    
    if (response.ok) {
      alert('Вы сдались. Партия завершена!');
      window.location.href = '/lobby';
    } else {
      alert('Ошибка: ' + (data.error || 'Не удалось сдаться'));
    }
  } catch (error) {
    console.error('Ошибка при сдаче:', error);
    alert('Ошибка подключения');
  }
});

// Функция для получения CSRF токена из cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}