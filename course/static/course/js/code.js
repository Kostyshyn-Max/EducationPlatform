function hide_result_popup(){
  document.getElementById("code-output").style.visibility = 'hidden';
}
document.addEventListener("DOMContentLoaded", function(event) {
  document.getElementById('id_username').placeholder = 'Імя користувача: ';
  document.getElementById('id_password').placeholder = 'Пароль: ';
  document.getElementById('register-form').querySelector('#id_username').placeholder = 'Імя користувача: ';
  document.getElementById('register-form').querySelector('#id_email').placeholder = 'Електронна пошта:  ';
  document.getElementById('register-form').querySelector('#id_password1').placeholder = 'Пароль: ';
  document.getElementById('register-form').querySelector('#id_password2').placeholder = 'Повторіть пароль: ';
});