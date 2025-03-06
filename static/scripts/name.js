// Obtener los elementos del formulario
const form = document.getElementById('form-nombre-apellido');
const nombreInput = document.getElementById('nombre');
const apellidoInput = document.getElementById('apellido');
const btnGuardar = document.getElementById('btn-guardar');

// Agregar un evento de clic al botón de guardar
btnGuardar.addEventListener('click', (e) => {
    e.preventDefault();
    // Obtener los valores del nombre y apellido
    const nombre = nombreInput.value.trim();
    const apellido = apellidoInput.value.trim();
    // Verificar si el usuario ha ingresado su nombre y apellido
    if (nombre === '' || apellido === '') {
        Swal.fire({
            title: '<span style="color: red">A D V E R T E N C I A</span>',
            text: 'Por favor, Ingrese su Nombre y Apellido',
            icon: 'warning',
        });
    } else {
        // Guardar los valores en el almacenamiento local
        localStorage.setItem('nombre_usuario', `${nombre} ${apellido}`);
        localStorage.setItem('version', '1.0'); // Agregar versión
        // Redireccionar a la ruta /inicio
        window.location.href = '/inicio';
    }
});

// Agregar un evento de carga de página para verificar si hay nombre guardado
window.addEventListener('load', () => {
    const nombreGuardado = localStorage.getItem('nombre_usuario');
    const versionGuardada = localStorage.getItem('version');
    const versionActual = '1.0'; // Versión actual

    if (versionGuardada !== versionActual) {
        // Si la versión guardada no coincide con la versión actual, borrar el usuario
        localStorage.removeItem('nombre_usuario');
        localStorage.removeItem('version');
    }

    if (!nombreGuardado && window.location.pathname === '/inicio') {
        // Si no hay nombre guardado y estamos en la página /inicio, redireccionar al index
        window.location.href = '/';
    } else if (nombreGuardado && window.location.pathname === '/inicio') {
        // Si hay nombre guardado y estamos en la página /inicio, mostrarlo en la página
        document.getElementById('bienvenido').innerHTML = `Bienvenido <span style="color: red">${nombreGuardado}</span>`;
    }
});