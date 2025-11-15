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
            window.location.href = '/';
        
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

// 1. Busca el contenedor que preparamos en el HTML
const cercaDeTiContainer = document.getElementById("cerca-de-ti-container");

// 2. Pide la ubicación al navegador
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
        function(position) {
            // ÉXITO: Tenemos la ubicación
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            // 3. Llama a la función para cargar publicaciones
            cargarPublicacionesCercanas(lat, lon);
        },
        function(error) {
            // ERROR: El usuario denegó el permiso
            cercaDeTiContainer.innerHTML = '<p style="padding-left: 1rem; color: #555;">No podemos mostrar ofertas cercanas sin tu permiso de ubicación.</p>';
        }
    );
} else {
    cercaDeTiContainer.innerHTML = '<p style="padding-left: 1rem; color: #555;">Tu navegador no soporta geolocalización.</p>';
}


// 4. Función que llama a nuestra API de Django
async function cargarPublicacionesCercanas(lat, lon) {
    try {
        // Llama a la nueva URL que creamos
        const response = await fetch(`/api/publicaciones_cercanas/?lat=${lat}&lon=${lon}`);
        
        if (!response.ok) {
            throw new Error('Error al cargar publicaciones');
        }
        
        const data = await response.json();
        
        // 5. Limpia el contenedor y muestra los resultados
        cercaDeTiContainer.innerHTML = '';
        
        if (data.publicaciones.length === 0) {
            cercaDeTiContainer.innerHTML = '<p style="padding-left: 1rem; color: #555;">No se encontraron publicaciones en un radio de 10 km.</p>';
            return;
        }

        // 6. Construye el HTML para cada publicación
        data.publicaciones.forEach(pub => {
            const article = document.createElement('article');
            article.className = 'listing-item';
            
            article.innerHTML = `
                <div class="listing-img-box">
                    <img src="${pub.imagen_url}" alt="${pub.descripcion}" style="width:100%; height:100%; object-fit:cover;">
                </div>
                <div class="listing-info-box">
                    <p class="listing-desc">${pub.descripcion}</p>
                    <p class="listing-price">$${pub.precio}</p>
                </div>
            `;
            cercaDeTiContainer.appendChild(article);
        });

    } catch (error) {
        console.error("Error al cargar publicaciones cercanas:", error);
        cercaDeTiContainer.innerHTML = '<p style="padding-left: 1rem; color: #555;">Error al cargar las publicaciones.</p>';
    }
}