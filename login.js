// login.js
const validCredentials = [
    { username: "admin", password: "soledemais" },
    { username: "Sucafina", password: "sucafinaesol" }
]; 

document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent form submission

    const inputUsername = document.getElementById("username").value;
    const inputPassword = document.getElementById("password").value;

    const isValidUser = validCredentials.some(
        credentials => credentials.username === inputUsername && credentials.password === inputPassword
    );

    if (isValidUser) {
        // Redirect to your main page (e.g., main.html)
        window.location.href = "map.html";
    } else {
        alert("Usuário ou senha estão incorretos");
    }
});