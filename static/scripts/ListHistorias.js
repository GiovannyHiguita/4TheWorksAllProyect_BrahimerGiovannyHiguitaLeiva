document.addEventListener('DOMContentLoaded', () => {
    fetch('/all/historias')
      .then(response => response.json())
      .then(data => {
        const historiasContainer = document.getElementById('historias');
        data.data.forEach(historia => {
          const historiaHTML = `
            <div class="card">
              <img src="${window.location.origin}/${historia.imagen}" class="card-img-top" alt="${historia.nombre_historia}">
              <div class="info_histo">
                <h5 class="card-title">${historia.nombre_historia}</h5>
                <p class="card-text">Año: ${historia.fecha_de_la_leyenda}</p>
                <a href="/InfoHistoria/${historia._id}" class="btn btn-primary">Editar historia</a>
              </div>
            </div>
          `;
          historiasContainer.innerHTML += historiaHTML;
        });
      })
      .catch(error => console.error('Error:', error));
  });