// Set theme before DOM is loaded to avoid FOUC

(function () {
  var html = document.documentElement;
  var savedTheme = localStorage.getItem('pw-theme');
  if (savedTheme) {
    html.setAttribute('data-theme', savedTheme);
  }
})();

function setButtonIcon(theme) {
  var themeToggle = document.getElementById('theme-toggle');
  var iconTemplateId = {
    light: 'moon-icon',
    dark: 'sun-icon',
  };
  if (themeToggle) {
    const iconTemplate = document.getElementById(iconTemplateId[theme === 'dark' ? 'dark' : 'light']);
    const clone = iconTemplate.content.cloneNode(true);
    themeToggle.innerHTML = '';
    themeToggle.appendChild(clone);
  }
}

// After DOM is loaded, set the toggle button character and register event listener
document.addEventListener('DOMContentLoaded', function () {
  var html = document.documentElement;
  var themeToggle = document.getElementById('theme-toggle');
  var savedTheme = localStorage.getItem('pw-theme');

  if (themeToggle) {
    if (savedTheme) {
      setButtonIcon(savedTheme);
    } else {
      var currentTheme = html.getAttribute('data-theme') || 'dark';
      setButtonIcon(currentTheme);
    }

    themeToggle.addEventListener('click', function () {
      var currentTheme = html.getAttribute('data-theme');
      var newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', newTheme);
      setButtonIcon(newTheme);
      localStorage.setItem('pw-theme', newTheme);
    });
  }
});
