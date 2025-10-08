const form = document.getElementById('login-form');
const email = document.getElementById('email');
const password = document.getElementById('password');
const error = document.getElementById('error');
const toggle = document.getElementById('toggle');
const year = document.getElementById('year');

if (year) year.textContent = new Date().getFullYear();

if (toggle && password) {
 toggle.addEventListener('click', () => {
  const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
  password.setAttribute('type', type);
  toggle.textContent = type === 'password' ? '👁️' : '🙈';
 });
}

if (form) {
 form.addEventListener('submit', (e) => {
  // Si usas autenticación del lado servidor, puedes quitar esta parte de demo
  // y dejar que Django procese normalmente.
  e.preventDefault();

  const validEmail = email.value.trim().match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);
  const validPass = password.value.length >= 6;

  if (!validEmail || !validPass) {
   error.style.display = 'block';
   return;
  }
  error.style.display = 'none';

  // Aquí harías submit real si quieres:
  // form.submit();

  // Demo:
  alert('¡Inicio de sesión correcto! (demo)');
 });
}
