import numpy as np
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
import cv2
import streamlit as st
from PIL import Image
import io
import base64

# Dicionário contendo cores Junguianas
cores_junguianas = {
    '1': {
        'cor': 'Preto',
        'rgb': (0, 0, 0),
        'anima_animus': 'A cor preta representa a sombra do inconsciente, simbolizando os aspectos desconhecidos e reprimidos de uma pessoa.',
        'sombra': 'A cor preta é a própria sombra, representando os instintos primordiais e os aspectos ocultos da personalidade.',
        'personalidade': 'A cor preta pode indicar uma personalidade enigmática, poderosa e misteriosa.',
        'diagnostico': 'O uso excessivo da cor preta pode indicar uma tendência à negatividade, depressão ou repressão emocional.'
    },
    # ... (outras cores Junguianas)
}

# Funções auxiliares
def rgb_to_cmyk(r, g, b):
    if (r == 0) and (g == 0) and (b == 0):
        return 0, 0, 0, 1
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255

    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    return c, m, y, k

def calculate_ml(c, m, y, k, total_ml):
    total_ink = c + m + y + k
    c_ml = (c / total_ink) * total_ml
    m_ml = (m / total_ink) * total_ml
    y_ml = (y / total_ink) * total_ml
    k_ml = (k / total_ink) * total_ml
    return c_ml, m_ml, y_ml, k_ml

def buscar_cor_proxima(rgb, cores_junguianas):
    distancias = []
    for cor_junguiana in cores_junguianas.values():
        cor_junguiana_rgb = cor_junguiana['rgb']
        distancia = np.sqrt(np.sum((np.array(rgb) - np.array(cor_junguiana_rgb)) ** 2))
        distancias.append(distancia)
    cor_proxima_index = np.argmin(distancias)
    return cores_junguianas[str(cor_proxima_index + 1)]

# Classe Canvas para manipulação de imagem
class Canvas():
    def __init__(self, src, nb_color, pixel_size=4000):
        self.src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
        self.nb_color = nb_color
        self.tar_width = pixel_size
        self.colormap = []

    def generate(self):
        im_source = self.resize()
        clean_img = self.cleaning(im_source)
        width, height, depth = clean_img.shape
        clean_img = np.array(clean_img, dtype="uint8") / 255
        quantified_image, colors = self.quantification(clean_img)
        canvas = np.ones(quantified_image.shape[:2], dtype="uint8") * 255

        for ind, color in enumerate(colors):
            self.colormap.append([int(c * 255) for c in color])
            mask = cv2.inRange(quantified_image, color, color)
            cnts = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            for contour in cnts:
                _, _, width_ctr, height_ctr = cv2.boundingRect(contour)
                if width_ctr > 10 and height_ctr > 10 and cv2.contourArea(contour, True) < -100:
                    cv2.drawContours(canvas, [contour], -1, (0, 0, 0), 1)
                    txt_x, txt_y = contour[0][0]
                    cv2.putText(canvas, '{:d}'.format(ind + 1), (txt_x, txt_y + 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        return canvas, colors, quantified_image

    def resize(self):
        (height, width) = self.src.shape[:2]
        if height > width:  # modo retrato
            dim = (int(width * self.tar_width / float(height)), self.tar_width)
        else:
            dim = (self.tar_width, int(height * self.tar_width / float(width)))
        return cv2.resize(self.src, dim, interpolation=cv2.INTER_AREA)

    def cleaning(self, picture):
        clean_pic = cv2.fastNlMeansDenoisingColored(picture, None, 10, 10, 7, 21)
        kernel = np.ones((5, 5), np.uint8)
        img_erosion = cv2.erode(clean_pic, kernel, iterations=1)
        img_dilation = cv2.dilate(img_erosion, kernel, iterations=1)
        return img_dilation

    def quantification(self, picture):
        width, height, depth = picture.shape
        flattened = np.reshape(picture, (width * height, depth))
        sample = shuffle(flattened)[:1000]
        kmeans = KMeans(n_clusters=self.nb_color).fit(sample)
        labels = kmeans.predict(flattened)
        new_img = self.recreate_image(kmeans.cluster_centers_, labels, width, height)
        return new_img, kmeans.cluster_centers_

    def recreate_image(self, codebook, labels, width, height):
        vfunc = lambda x: codebook[labels[x]]
        out = vfunc(np.arange(width * height))
        return np.resize(out, (width, height, codebook.shape[1]))

# Configurações da barra lateral
st.sidebar.title("Criação das Paletas de cores e Tela numerada")

# Separador
st.sidebar.write("---")

# Seção de Informações do Autor
st.sidebar.header("Informações do Autor")
st.sidebar.image("clube.png", use_column_width=True)
st.sidebar.write("Nome: Marcelo Claro")
st.sidebar.write("Email: marceloclaro@geomaker.org")
st.sidebar.write("WhatsApp: (88) 98158-7145")

# Separador
st.sidebar.write("---")

# Seção de Configurações
st.sidebar.header("Configurações da Aplicação")
uploaded_file = st.sidebar.file_uploader("Escolha uma imagem", type=["jpg", "png"])
nb_color = st.sidebar.slider('Escolha o número de cores para pintar', min_value=1, max_value=100, value=2, step=1)
total_ml = st.sidebar.slider('Escolha o total em ml da tinta de cada cor', min_value=1, max_value=1000, value=10, step=1)
pixel_size = st.sidebar.slider('Escolha o tamanho do pixel da pintura', min_value=500, max_value=8000, value=4000, step=100)

if st.sidebar.button('Gerar'):
    if uploaded_file is not None:
        pil_image = Image.open(uploaded_file)
        if 'dpi' in pil_image.info:
            dpi = pil_image.info['dpi']
            st.write(f'Resolução da imagem: {dpi} DPI')

            cm_per_inch = pixel_size
            cm_per_pixel = cm_per_inch / dpi[0]
            st.write(f'Tamanho de cada pixel: {cm_per_pixel:.4f} centímetros')

        src = np.array(pil_image)

        canvas = Canvas(src, nb_color, pixel_size)
        result, colors, segmented_image = canvas.generate()

        segmented_image = (segmented_image * 255).astype(np.uint8)
        segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB)

        st.image(segmented_image, caption='Imagem Segmentada', use_column_width=True)
        cor_dominante = buscar_cor_proxima(colors[0], cores_junguianas)
        st.write("---")
        st.image(result, caption='Imagem para pintar', use_column_width=True)
        st.write("---")

        cor_hex = '#%02x%02x%02x' % tuple(cor_dominante['rgb'])
        cmyk = rgb_to_cmyk(*cor_dominante['rgb'])
        ml_values = calculate_ml(*cmyk, total_ml)

        st.write(f"Cor dominante: {cor_dominante['cor']}")
        st.write(f"Anima/Animus: {cor_dominante['anima_animus']}")
        st.write(f"Sombra: {cor_dominante['sombra']}")
        st.write(f"Personalidade: {cor_dominante['personalidade']}")
        st.write(f"Diagnóstico: {cor_dominante['diagnostico']}")
        st.write(f"Cor em hexadecimal: {cor_hex}")
        st.write(f"Valores CMYK: C: {cmyk[0]:.2f}, M: {cmyk[1]:.2f}, Y: {cmyk[2]:.2f}, K: {cmyk[3]:.2f}")
        st.write(f"Quantidade de tinta (ml): C: {ml_values[0]:.2f}, M: {ml_values[1]:.2f}, Y: {ml_values[2]:.2f}, K: {ml_values[3]:.2f}")

        # Baixar imagem
        st.write("---")
        result_pil = Image.fromarray(result)
        buffer = io.BytesIO()
        result_pil.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()

        href = f'<a href="data:image/png;base64,{img_str}" download="tela_para_pintar.png">Baixar imagem para pintar</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.sidebar.error("Por favor, carregue uma imagem.")
