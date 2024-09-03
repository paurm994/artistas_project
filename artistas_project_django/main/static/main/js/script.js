// script.js
document.addEventListener('DOMContentLoaded', function() {
    const esArtistaCheckbox = document.querySelector('#id_es_artista');
    const esCompradorCheckbox = document.querySelector('#id_es_comprador');

    function toggleFormFields() {
        if (esArtistaCheckbox.checked) {
            esCompradorCheckbox.checked = false;
            // Mostrar campos específicos para artistas
            // Por ejemplo: document.querySelector('#campoParaArtistas').style.display = 'block';
        } else if (esCompradorCheckbox.checked) {
            esArtistaCheckbox.checked = false;
            // Mostrar campos específicos para compradores
            // Por ejemplo: document.querySelector('#campoParaCompradores').style.display = 'block';
        }
    }

    esArtistaCheckbox.addEventListener('change', toggleFormFields);
    esCompradorCheckbox.addEventListener('change', toggleFormFields);
});
