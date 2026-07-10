(function () {
  function removeOldLanguageWidgets() {
    document.querySelectorAll(
      '.saci-lang-toggle, .lang-toggle, .language-toggle, #saci-lang-toggle-style, #saci-lang-toggle-script'
    ).forEach(function (el) {
      el.remove();
    });
  }

  function setLang(lang) {
    localStorage.setItem('saci-lang', lang);

    document.querySelectorAll('[data-lang-switch]').forEach(function (btn) {
      btn.classList.toggle('is-active', btn.getAttribute('data-lang-switch') === lang);
    });

    document.querySelectorAll('[data-tr][data-en]').forEach(function (el) {
      var value = el.getAttribute(lang === 'en' ? 'data-en' : 'data-tr');
      if (value) el.innerHTML = value;
    });

    document.documentElement.setAttribute('lang', lang === 'en' ? 'en' : 'tr');
  }

  document.addEventListener('DOMContentLoaded', function () {
    removeOldLanguageWidgets();

    var lang = localStorage.getItem('saci-lang') || 'tr';
    setLang(lang);

    document.querySelectorAll('[data-lang-switch]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        setLang(btn.getAttribute('data-lang-switch'));
      });
    });
  });
})();
