// 1. Автоматичне оновлення сторінки кожні 30 секунд
// Це корисно, щоб бачити, як просувається черга без ручного оновлення
if (window.location.pathname.includes('/queues/')) {
    setTimeout(function() {
        location.reload();
    }, 30000); // 30000 мс = 30 секунд
}

// 2. Підтвердження перед викликом "Наступного"
// Щоб хазяїн черги випадково не пропустив людину
document.addEventListener('DOMContentLoaded', function() {
    const nextButtons = document.querySelectorAll('form[action$="/next"] button');

    nextButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Ви впевнені, що хочете викликати наступного учасника?')) {
                e.preventDefault(); // Скасовує відправку форми
            }
        });
    });
});

// 3. Плавне зникнення повідомлень про помилки
setTimeout(() => {
    const errorBox = document.querySelector('.error-message');
    if (errorBox) {
        errorBox.style.transition = 'opacity 1s ease';
        errorBox.style.opacity = '0';
        setTimeout(() => errorBox.remove(), 1000);
    }
}, 5000);