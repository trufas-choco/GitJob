document.addEventListener("DOMContentLoaded", function() {

    const loginForm = document.getElementById("login-form");
    const phone = document.getElementById("phone");
    const password = document.getElementById("password");
    const errorMessage = document.getElementById("error-message-login");

   
    loginForm.addEventListener("submit", async function(event) {
    
        event.preventDefault(); 
        
        errorMessage.textContent = "";

        
        const phoneValue = phone.value;
        const passwordValue = password.value;

        if (!phoneValue || !passwordValue) {
            mostrarError("Por favor, ingrese teléfono y contraseña.");
            return;
        }


        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
            
                },
                body: JSON.stringify({
                    phone: phoneValue,
                    password: passwordValue
                })
            });

            const data = await response.json();

            if (response.ok) {
        
                console.log("Login exitoso. Redirigiendo...");
                window.location.href = data.redirectUrl; 
            } else {
               
                mostrarError(data.error); 
            }

        } catch (error) {
           
            console.error("Error de conexión:", error);
            mostrarError("Error de conexión. Intente más tarde.");
        }
    });

   
    function mostrarError(mensaje) {
        errorMessage.textContent = mensaje;
    }
});