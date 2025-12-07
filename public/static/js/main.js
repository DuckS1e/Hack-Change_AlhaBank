// main.js — основной скрипт для AI Bank Advisor

document.addEventListener('DOMContentLoaded', function () {
  // 1. Активная ссылка в навигации
  const currentLocation = window.location.pathname;
  const navLinks = document.querySelectorAll('nav a');

  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentLocation) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  // 2. Плавное появление страниц
  const pageContent = document.querySelector('main');
  if (pageContent) {
    pageContent.style.opacity = '0';
    pageContent.style.transition = 'opacity 0.5s ease-in';
    setTimeout(() => {
      pageContent.style.opacity = '1';
    }, 100);
  }

  // 3. Подтверждение выхода
  const logoutLinks = document.querySelectorAll('a[href$="/logout"]');
  logoutLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      const confirmed = confirm('Вы уверены, что хотите выйти?');
      if (!confirmed) {
        e.preventDefault();
      }
    });
  });

  // 4. Подсказки для SHAP-значений (при наведении)
  const shapValues = document.querySelectorAll('.shap-value');
  shapValues.forEach(el => {
    const value = el.textContent.trim();
    if (value.startsWith('+')) {
      el.title = 'Положительный вклад в прогноз';
    } else if (value.startsWith('–') || value.startsWith('-')) {
      el.title = 'Отрицательный вклад в прогноз';
    }
  });

  // 5. Копирование строки сессии (если будет)
  const sessionCode = document.querySelector('.session-code');
  if (sessionCode) {
    sessionCode.style.cursor = 'pointer';
    sessionCode.addEventListener('click', () => {
      navigator.clipboard.writeText(sessionCode.textContent).then(() => {
        alert('Строка сессии скопирована!');
      });
    });
  }
});
