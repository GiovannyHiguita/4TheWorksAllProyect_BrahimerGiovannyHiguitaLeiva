document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('borrar-cache').addEventListener('click', () => {
        Swal.fire({
            title: '¿Estás seguro?',
            text: 'Se borrarán todos los datos guardados',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, borrar',
            cancelButtonText: 'No, cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                localStorage.clear();
                sessionStorage.clear();
                window.location.href = '/';
            }
        });
    });

    // Verificar si hay nombre guardado
    const nombreGuardado = localStorage.getItem('nombre_usuario');
    const rutaActual = window.location.pathname;

    if (!nombreGuardado || nombreGuardado === null) {
        if (rutaActual !== '/') {
            window.location.href = '/';
        }
    }
});