document.addEventListener("DOMContentLoaded", function() {

   
    const signupForm = document.getElementById("signup-form");
    const password = document.getElementById("new-password");
    const confirmPassword = document.getElementById("confirm-password");
    const phone = document.getElementById("phone");
    const errorMessage = document.getElementById("error-message");
    
   
    signupForm.addEventListener("submit", function(event) {
        
        event.preventDefault(); 
     
        errorMessage.textContent = "";

        const passValue = password.value;
        const confirmPassValue = confirmPassword.value;
        const phoneValue = phone.value;

        if (passValue !== confirmPassValue) {
            mostrarError("Error: Las contraseñas no coinciden.");
            return; 
        }

       
        const passwordErrors = [];
        
        if (passValue.length < 8) {
            passwordErrors.push("Debe tener al menos 8 caracteres.");
        }
        if (!/[A-Z]/.test(passValue)) {
            passwordErrors.push("Debe tener al menos una mayúscula (A-Z).");
        }
        if (!/[a-z]/.test(passValue)) {
            passwordErrors.push("Debe tener al menos una minúscula (a-z).");
        }
        if (!/[0-9]/.test(passValue)) {
            passwordErrors.push("Debe tener al menos un número (0-9).");
        }

        if (passwordErrors.length > 0) {
            // \n es un salto de línea
            mostrarError("La contraseña no es segura:\n" + passwordErrors.join("\n"));
            return;
        }

        const phoneRegex = /^[0-9]{9}$/; 
        if (!phoneRegex.test(phoneValue.replace(/\s/g, ''))) { // quitamos espacios
            mostrarError("El formato del teléfono debe ser '9 1234 5678'.");
            return;
        }

      
        console.log("Formulario validado, enviando al backend...");
        
     
        signupForm.submit();
    });

    function mostrarError(mensaje) {
        errorMessage.innerHTML = mensaje.replace(/\n/g, '<br>');
    }
});