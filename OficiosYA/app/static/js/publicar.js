document.addEventListener('DOMContentLoaded', function() {

    const latInput = document.getElementById('latitude');
    const lonInput = document.getElementById('longitude');

    if (navigator.geolocation) {
        // Le pide al navegador la ubicación
        navigator.geolocation.getCurrentPosition(
            function(position) {
                // ÉXITO: El usuario aceptó
                console.log('Ubicación obtenida:', position.coords.latitude, position.coords.longitude);
                // Rellenamos los campos ocultos del formulario
                if(latInput) latInput.value = position.coords.latitude;
                if(lonInput) lonInput.value = position.coords.longitude;
            },
            function(error) {
                // ERROR: El usuario denegó el permiso o hubo un fallo
                console.warn('Error de geolocalización:', error.message);
            }
        );
    } else {
        console.warn('La geolocalización no es soportada por este navegador.');
    }
    const imagenInput = document.getElementById('imagen');
    // Obtenemos las 3 cajas de vista previa
    const previewBoxes = [
        { img: document.getElementById('preview-1'), icon: document.querySelector('label[for="imagen"]:nth-of-type(1) svg') },
        { img: document.getElementById('preview-2'), icon: document.querySelector('label[for="imagen"]:nth-of-type(2) svg') },
        { img: document.getElementById('preview-3'), icon: document.querySelector('label[for="imagen"]:nth-of-type(3) svg') }
    ];

    if (imagenInput) {
        imagenInput.addEventListener('change', function(event) {
            const files = event.target.files;
            
            // 1. Limpiar todas las vistas previas primero
            previewBoxes.forEach(p => {
                p.img.src = '';
                p.img.style.display = 'none';
                p.icon.style.display = 'block'; // Muestra el icono
            });

            // 2. Mostrar las nuevas imágenes (hasta 3)
            for (let i = 0; i < files.length && i < 3; i++) {
                const file = files[i];
                const reader = new FileReader();
                const currentPreview = previewBoxes[i];
                
                reader.onload = function(e) {
                    currentPreview.img.src = e.target.result;
                    currentPreview.img.style.display = 'block'; // Muestra la imagen
                    currentPreview.icon.style.display = 'none'; // Oculta el icono
                }
                
                reader.readAsDataURL(file);
            }
        });
    }
});