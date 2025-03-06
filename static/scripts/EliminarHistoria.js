document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('EliminarHistoria').addEventListener('click', () => {
        const idHistoria = document.getElementById('EliminarHistoria').getAttribute('data-id');
        Swal.fire({
            title: '¿Estás seguro?',
            text: 'Se eliminará la historia seleccionada',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'No, cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(`/InfoHistoria/${idHistoria}`, {
                    method: 'DELETE'
                })
                .then(() => {
                    window.location.href = '/inicio';
                });
            }
        });
    });
});
