// Esperar a que todo el HTML esté cargado
document.addEventListener("DOMContentLoaded", async function() {

    // 1. Identificar el elemento del saludo
    const welcomeElement = document.getElementById("welcome-user");

    // 2. Pedir los datos del usuario al backend
    try {
        const response = await fetch('/api/user/me', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                // (Mi backend usará la cookie de sesión para identificar al usuario)
            }
        });

        if (response.ok) {
            // ÉXITO: El backend me envió los datos
            const userData = await response.json();
            
            // Actualizamos el saludo (usando el 'first_name' que guardamos)
            welcomeElement.textContent = `Bienvenid@, ${userData.first_name}`;
        
        } else if (response.status === 401) {
            // ERROR: No autorizado (no ha iniciado sesión)
            // Lo redirigimos de vuelta al login
            console.warn("Usuario no autenticado. Redirigiendo al login.");
            window.location.href = 'index.html';
        
        } else {
            // Otro tipo de error del servidor
            welcomeElement.textContent = "Bienvenid@";
        }

    } catch (error) {
        // Error de red o si mi backend está caído
        console.error("Error de conexión:", error);
        welcomeElement.textContent = "Bienvenid@";
    }
});