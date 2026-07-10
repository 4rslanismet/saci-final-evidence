
document.addEventListener("DOMContentLoaded", () => {
    const lang = localStorage.getItem('saci-lang') || 'tr';
    document.documentElement.lang = lang;
    
    document.querySelectorAll('.lang-switch button').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const selected = e.target.getAttribute('data-lang');
            document.documentElement.lang = selected;
            localStorage.setItem('saci-lang', selected);
        });
    });
});
