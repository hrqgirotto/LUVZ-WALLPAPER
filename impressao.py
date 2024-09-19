import re
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
import json
import os

class Musica:
    def __init__(self, link):
        isTrack = ('track' in link)
        self.link = link
        self.nomeMusica = ''
        self.nomeArtista = ''
        self.duracao = 0
        self.linkImgCapa = ''
        self.linkImgScan = ''
        self.isTrack = isTrack
        self.setInformacoes()

    def setInformacoes(self):
        informacoes = self.getInfomacoes()
        self.nomeMusica = self.rewriteName(informacoes['name'])
        self.nomeArtista = informacoes['artists'][0]['name']
        self.linkImgCapa = informacoes['album']['images'][0]['url']
        self.linkImgScan = self.getLinkImgScan(informacoes)
        self.duracao = informacoes['duration_ms']

    def getLinkImgScan(self, informacoes):
        track = informacoes['uri'].split(':')[2]
        return f'https://scannables.scdn.co/uri/plain/png/000000/white/640/spotify:track:{track}'

    def helperTrack(self):
        token = self.getToken()
        html = requests.get(f'https://api.spotify.com/v1/tracks/{self.getTrack()}',
                            headers={
                                'Authorization': f"{token['token_type']} {token['access_token']}"
                            })
        informacoes = json.loads(html.content)
        return informacoes

    def helperPlaylist(self):
        token = self.getToken()
        html = requests.get(f'https://api.spotify.com/v1/playlists/{self.getPlaylist()}',
                            headers={
                                'Authorization': f"{token['token_type']} {token['access_token']}"
                            })
        tmp_info = json.loads(html.content)
        link_musica1 = tmp_info['tracks']['items'][0]['track']['external_urls']['spotify']
        informacoes = Musica(link_musica1).getInfomacoes()
        informacoes['album']['images'][0]['url'] = tmp_info['images'][0]['url']
        return informacoes

    def getInfomacoes(self):
        if self.isTrack:
            return self.helperTrack()
        else:
            return self.helperPlaylist()

    def getToken(self):
        html = requests.get('https://www.spotifycodes.com/getToken.php').content
        token = json.loads(html)
        return token

    def getTrack(self):
        index_str_track = self.link.index('/track/')
        return str(self.link[index_str_track + 7:].lstrip('?'))

    def getPlaylist(self):
        index_str_playlist = self.link.index('/playlist/')
        return str(self.link[index_str_playlist + 10:].lstrip('?'))

    def getDuracao(self):
        tempo = int(self.duracao / 1000)
        minutos = tempo // 60
        segundos = tempo % 60
        if segundos <= 9:
            return f'{minutos}:0{segundos}'
        else:
            return f'{minutos}:{segundos}'

    def rewriteName(self, nome: str):
        with open("excecoes.txt", 'r', encoding='utf-8-sig') as arquivo_texto:
            for item in arquivo_texto.readlines()[0].split(","):
                if (item.upper() in nome.upper()):
                    return nome
        return re.sub(r"- .*| \(.*", "", nome)


class Quadro:
    def __init__(self, link):
        self.musica = Musica(link)
        self.heightCompensation = 0
        self.width = 1080  # Ajustado para wallpaper
        self.height = 1920  # Ajustado para wallpaper
        self.scanWidth = 512  # Ajustado para manter a proporção do código
        self.scanHeight = 128
        self.textColor = (255, 255, 255)
        self.fontTitle = 'FUTURA_HEAVY_FONT.TTF'
        self.fontMusic = 'FUTURA_LIGHT_BT.TTF'
        self.fontDuration = 'FUTURA_MEDIUM_BT.TTF'
        self.templateName = 'moldura.webp'

    def getImagemCapa(self):
        response = requests.get(self.musica.linkImgCapa)
        buffer = BytesIO(response.content)
        return buffer

    def getImagemScan(self):
        response = requests.get(self.musica.linkImgScan)
        buffer = BytesIO(response.content)
        return Image.open(buffer).convert("RGBA")

    def getFontNomeMusica(self):
        tamanhoFonte = 66
        config = {
            'font-family': os.path.join('static', 'fonts', self.fontTitle),
        }
        valorMaximo = 800  # Ajustado para se adequar ao formato wallpaper
        font = ImageFont.truetype(config['font-family'], tamanhoFonte)
        initialSize = font.getbbox(self.musica.nomeMusica)[1]
        while font.getbbox(self.musica.nomeMusica)[2] > valorMaximo:
            tamanhoFonte -= 5
            self.heightCompensation = (initialSize - font.getbbox(self.musica.nomeMusica)[1]) / 2
            font = ImageFont.truetype(config['font-family'], tamanhoFonte)
        return font

    def getFontNomeArtista(self):
        config = {
            'font-family': os.path.join('static', 'fonts', self.fontMusic),
            'font-size': 50
        }
        return ImageFont.truetype(config['font-family'], config['font-size'])

    def getFontDuracao(self):
        config = {
            'font-family': os.path.join('static', 'fonts', self.fontDuration),
            'font-size': 34
        }
        return ImageFont.truetype(config['font-family'], config['font-size'])

    def removeBackGround(self, img):
        """
        Remove o fundo preto de uma imagem, transformando-o em transparente sem afetar a qualidade do código.
        """
        img = img.convert('RGBA')
        data = img.getdata()
        new_data = []

        for pixel in data:
            if pixel[:3] == (0, 0, 0):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(pixel)

        img.putdata(new_data)
        return img

    def resize_image_high_quality(self, image, size):
        return image.resize(size, Image.LANCZOS)

    def centerXImage(self, dim):
        x, y = dim
        return (self.width // 2 - x // 2, y)

    def centerFont(self, font, text, y):
        return self.centerXImage((font.getbbox(text)[2], y))

    def buildChaveiro(self, user_img=None, couple_name=None, relationship_date=None):
        # Carrega o template original sem modificar o fundo
        template = Image.open(os.path.join('static', self.templateName)).convert('RGBA')
        template = template.resize((self.width, self.height), Image.LANCZOS)

        # Se uma imagem de usuário for fornecida, use-a como fundo
        if user_img:
            user_img = self.resize_image_high_quality(user_img.convert('RGBA'), (self.width, self.height))
            base = Image.alpha_composite(user_img, template)  # Preserva o fundo da moldura
        else:
            base = template

        # Define os textos a serem usados na imagem
        nome_musica = couple_name if couple_name else self.musica.nomeMusica
        nome_artista = relationship_date if relationship_date else self.musica.nomeArtista

        # Aplica removeBackGround apenas ao scan do Spotify Code
        imgScan = self.resize_image_high_quality(self.getImagemScan(), (self.scanWidth, self.scanHeight))
        imgScan = self.removeBackGround(imgScan)  # Aplicando a função apenas no scan

        draw = ImageDraw.Draw(base)
        fontMusica = self.getFontNomeMusica()
        fontArtist = self.getFontNomeArtista()

        # Adiciona o nome da música ou do casal
        draw.text(self.centerFont(fontMusica, nome_musica, 1320),  # Ajuste a posição conforme necessário
                  nome_musica, self.textColor, font=fontMusica)

        # Adiciona o nome do artista ou a data
        draw.text(self.centerFont(fontArtist, nome_artista, 1400), nome_artista,
                  self.textColor, font=fontArtist)

        # Adiciona a duração da música
        draw.text((810, 1440), self.musica.getDuracao(), self.textColor, font=self.getFontDuracao())

        # Adiciona o scan do Spotify Code na posição desejada sem alterar o fundo da moldura
        base.paste(imgScan, self.centerXImage((self.scanWidth, 480)), imgScan)

        return base
