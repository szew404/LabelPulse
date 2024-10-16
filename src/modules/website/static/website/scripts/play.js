let currentAudio = null;
let currentButton = null; // Agregado para mantener referencia al botón actual

document.querySelectorAll('.play-btn').forEach(button => {
    button.addEventListener('click', function () {
        const audioFile = this.getAttribute('data-file');

        // If there is a current audio playing
        if (currentAudio) {
            if (currentButton === this) {
                // If the same track is clicked again, stop it
                currentAudio.pause();
                currentAudio.currentTime = 0; // Reset the audio to the beginning

                // Revert the button text and class
                this.textContent = '▶'; // Cambiar el texto a "Play"
                this.classList.remove('playing'); // Remover la clase "playing"
                currentAudio = null; // Reiniciar currentAudio
                currentButton = null; // Reiniciar currentButton
                return; // Salir de la función
            } else {
                // Pause the current audio if a different track is clicked
                currentAudio.pause();
                currentAudio.currentTime = 0; // Reset the audio to the beginning

                // Revert the button text and class for the previous track
                const previousButton = currentButton; // Guardar referencia al botón anterior
                if (previousButton) {
                    previousButton.textContent = '▶'; // Cambiar el texto de vuelta a "Play"
                    previousButton.classList.remove('playing'); // Remover la clase "playing"
                }
            }
        }

        // Create a new Audio object for the selected track
        currentAudio = new Audio(audioFile);
        currentButton = this; // Guardar referencia al botón actual

        // Cambiar el texto del botón a "Reproduciendo"
        this.textContent = '||'; // Cambiar a "Reproduciendo"
        this.classList.add('playing'); // Agregar clase para aplicar estilos diferentes

        // Play the selected track
        currentAudio.play();

        // Agregar un evento para cuando el audio termine
        currentAudio.addEventListener('ended', () => {
            this.textContent = '▶'; // Cambiar de vuelta a "Play" cuando termine
            this.classList.remove('playing'); // Remover clase "playing"
            currentAudio = null; // Reiniciar currentAudio
            currentButton = null; // Reiniciar currentButton
        });
    });
});
