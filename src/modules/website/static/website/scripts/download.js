document.querySelectorAll('.download-link').forEach(function (link) {
    link.addEventListener('click', function (event) {
        event.preventDefault();  // Evita la redirección
        const url = link.getAttribute('href');

        // Obtener los valores de los atributos data
        const trackArtist = link.getAttribute('data-artist');
        const trackTitle = link.getAttribute('data-title');

        // Descarga el archivo usando fetch
        fetch(url)
            .then(response => response.blob())
            .then(blob => {
                const a = document.createElement('a');
                const fileUrl = window.URL.createObjectURL(blob);

                a.href = fileUrl;
                a.download = `${trackArtist} - ${trackTitle}`;  // Asigna el nombre con track_artist y track_title
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(fileUrl);  // Limpia la URL temporal
                document.body.removeChild(a);
            })
            .catch(error => console.error('Error al descargar el archivo:', error));
    });
});
