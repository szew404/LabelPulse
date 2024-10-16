let currentAudio = null;
let currentButton = null;
let currentProgressBar = null; // Agregado para mantener referencia a la barra de progreso

document.querySelectorAll('.play-btn').forEach((button, index) => {
    button.addEventListener('click', function () {
        const audioFile = this.getAttribute('data-file');
        const progressBar = document.getElementById(`progress-bar-${index + 1}`);

        // If there is a current audio playing
        if (currentAudio) {
            if (currentButton === this) {
                // If the same track is clicked again, stop it
                currentAudio.pause();
                currentAudio.currentTime = 0;

                // Revert the button text and class
                this.textContent = '▶';
                this.classList.remove('playing');
                currentAudio = null;
                currentButton = null;
                currentProgressBar = null; // Reiniciar la barra de progreso
                return;
            } else {
                // Pause the current audio if a different track is clicked
                currentAudio.pause();
                currentAudio.currentTime = 0;

                // Revert the button text and class for the previous track
                const previousButton = currentButton;
                if (previousButton) {
                    previousButton.textContent = '▶';
                    previousButton.classList.remove('playing');
                }
            }
        }

        // Create a new Audio object for the selected track
        currentAudio = new Audio(audioFile);
        currentButton = this;
        currentProgressBar = progressBar; // Guardar referencia a la barra de progreso actual

        // Cambiar el texto del botón a "Reproduciendo"
        this.textContent = '||';
        this.classList.add('playing');

        // Play the selected track
        currentAudio.play();

        // Actualizar la barra de progreso mientras se reproduce
        currentAudio.addEventListener('timeupdate', () => {
            const progress = (currentAudio.currentTime / currentAudio.duration) * 100;
            currentProgressBar.value = progress;
        });

        // Mover manualmente la barra de progreso
        currentProgressBar.addEventListener('input', function () {
            currentAudio.currentTime = (this.value / 100) * currentAudio.duration;
        });

        // Agregar un evento para cuando el audio termine
        currentAudio.addEventListener('ended', () => {
            this.textContent = '▶';
            this.classList.remove('playing');
            currentAudio = null;
            currentButton = null;
            currentProgressBar.value = 0; // Resetear la barra de progreso
        });
    });
});
