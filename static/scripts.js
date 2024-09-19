function scrollToImage() {
        // Aguarda um tempo para que a imagem gerada seja carregada antes de rolar
        setTimeout(() => {
            const imagePreview = document.getElementById('imagePreview');
            imagePreview.scrollIntoView({ behavior: 'smooth' });
        }, 1000); // Ajuste o tempo de espera conforme necessário (em milissegundos)
    }

    document.getElementById('photo').addEventListener('change', function() {
        var fileName = this.files[0] ? this.files[0].name : 'Nenhum arquivo selecionado';
        document.getElementById('file-upload-name').textContent = fileName;
    });

 // Exibe o pop-up ao clicar no botão "Como pego?"
document.getElementById('infoButton').onclick = function() {
    document.getElementById('tutorialPopup').style.display = 'flex';
};

// Fecha o pop-up ao clicar no botão de fechar
document.getElementById('closePopup').onclick = function() {
    document.getElementById('tutorialPopup').style.display = 'none';
};

// Fecha o pop-up ao clicar fora dele
window.onclick = function(event) {
    const popup = document.getElementById('tutorialPopup');
    if (event.target === popup) {
        popup.style.display = 'none';
    }
};
