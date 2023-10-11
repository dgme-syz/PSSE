// csrf.js

export function getCsrfTokenFromCookies() {
    const cookies = document.cookie.split('; ');
    for (const cookie of cookies) {
      const [name, value] = cookie.split('=');
      if (name === 'csrftoken') {
        return value;
      }
    }
    return '';
}
  