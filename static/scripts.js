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
    