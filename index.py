from flask import Flask, request, send_file, render_template
from impressao import Quadro
from io import BytesIO
from PIL import Image
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Obtém o link do Spotify e a imagem do usuário
        link = request.form.get('spotify_link')
        user_image = request.files['photo']
        user_img = Image.open(user_image.stream)

        # Captura os campos opcionais
        couple_name = request.form.get('couple_name')  # Nome do casal
        relationship_date = request.form.get('relationship_date')  # Data do namoro
        
        # Formata a data para o formato DD/MM/YYYY, se estiver preenchida
        if relationship_date:
            try:
                relationship_date = datetime.strptime(relationship_date, '%Y-%m-%d').strftime('%d/%m/%Y')
            except ValueError:
                pass  # Se a data não estiver no formato correto, mantenha como está

        # Cria o objeto Quadro e gera a imagem, passando os campos opcionais
        quadro = Quadro(link)
        image = quadro.buildChaveiro(user_img=user_img, couple_name=couple_name, relationship_date=relationship_date)

        # Salva a imagem em um buffer para enviar de volta ao cliente
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        return send_file(buffer, mimetype='image/png')

    except Exception as e:
        print(f"Erro ao processar solicitação: {str(e)}")
        return f"Ocorreu um erro ao processar sua solicitação: {str(e)}", 500
    
#if __name__ == '__main__':#
    #app.run(debug=True)#