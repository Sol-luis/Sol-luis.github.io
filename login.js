// login.js
const validUsername = "admin"; 
const validPassword = "soledemais"; 

document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent form submission

    const inputUsername = document.getElementById("username").value;
    const inputPassword = document.getElementById("password").value;

   // Check if both username and password are correct
   if (inputUsername === validUsername && inputPassword === validPassword) {
    // Redirect to your main page (e.g., main.html)
    window.location.href = "main.html";
} else {
    alert("Usuário ou senha estão incorretos");
}
});