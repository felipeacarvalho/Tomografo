import os
import cv2
import numpy as np
from skimage.transform import radon
from skimage import exposure
from scipy.ndimage import median_filter, gaussian_filter  # Adição de filtro Gaussiano
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Diretórios
dir_imgs = "imgsCrop"  # Diretório de entrada
dir_sinogramas = "sinogramas"  # Diretório para salvar sinogramas
dir_transformadas = "transformadas_radon"  # Diretório para salvar transformadas de Radon

# Criar diretórios, se necessário
os.makedirs(dir_sinogramas, exist_ok=True)
os.makedirs(dir_transformadas, exist_ok=True)

# Listar e ordenar as imagens no diretório
imagens = sorted([f for f in os.listdir(dir_imgs) if f.endswith('.jpg')])

# Número de imagens por grupo (cada sinograma será formado por 99 imagens)
grupo_tamanho = 99
transformadas_radon = []  # Lista para armazenar as transformadas de Radon

# Processar as imagens em grupos
for i in range(0, len(imagens), grupo_tamanho):
    grupo = imagens[i:i + grupo_tamanho]
    sinograma_grupo = []

    # Processar cada imagem do grupo
    for img_nome in grupo:
        img_path = os.path.join(dir_imgs, img_nome)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        # Adicionar a imagem ao sinograma (horizontalmente)
        sinograma_grupo.append(img)

    # Empilhar horizontalmente para formar o sinograma
    sinograma = np.hstack(sinograma_grupo)

    # Salvar o sinograma
    sinograma_path = os.path.join(dir_sinogramas, f"sinograma_{i//grupo_tamanho:04d}.png")
    plt.imsave(sinograma_path, sinograma, cmap='gray')

    # Calcular a Transformada de Radon
    theta = np.linspace(0., 180., sinograma.shape[1], endpoint=False)
    transformada = radon(sinograma, theta=theta, circle=False)  # *Remover a borda escura usando circle=False*

    # *Aplicar filtro de mediana para reduzir ruído*
    transformada_filtered = median_filter(transformada, size=3)  # Filtro de mediana com janela 3x3

    # *Aplicar filtro gaussiano para suavizar ainda mais*
    transformada_filtered = gaussian_filter(transformada_filtered, sigma=1)  # Suavização adicional com filtro gaussiano

    # Normalizar para o intervalo [0, 1]
    transformada_normalized = (transformada_filtered - np.min(transformada_filtered)) / (np.max(transformada_filtered) - np.min(transformada_filtered))

    # Melhorar o contraste usando equalização de histograma
    transformada_contrast = exposure.equalize_adapthist(transformada_normalized, clip_limit=0.03)

    # Salvar a transformada de Radon com contraste ajustado
    transformada_path = os.path.join(dir_transformadas, f"radon_{i//grupo_tamanho:04d}.png")
    plt.imsave(transformada_path, transformada_contrast, cmap='gray')

    # Adicionar a transformada à lista para visualização 3D
    transformadas_radon.append(transformada_contrast)

# Visualizar o objeto 3D com espessura de 2 mm por camada
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Parâmetros ajustáveis
light_threshold = 0.9  # Ajuste o limite para partes mais claras (para simular luz)
dark_threshold = 0.75   # Ajuste o limite para as partes mais escuras (para detalhes profundos)
thickness = 2  # Espessura em mm de cada camada
sampling_factor = 0.002  # Fator de amostragem (2% dos pontos serão plotados)

# Processar cada camada de transformada de Radon
for idx, radon_img in enumerate(transformadas_radon):
    # Normalizar a intensidade para valores entre 0 e 1
    radon_img_normalized = (radon_img - np.min(radon_img)) / (np.max(radon_img) - np.min(radon_img))

    # Criar máscara baseada nos thresholds
    mask_included = (radon_img_normalized >= dark_threshold) & (radon_img_normalized < light_threshold)

    # Filtrar apenas os pontos incluídos
    radon_img_filtered = radon_img_normalized[mask_included]

    # Coordenadas 2D para criar o volume
    x, y = np.meshgrid(np.arange(radon_img_normalized.shape[1]), np.arange(radon_img_normalized.shape[0]))
    x_filtered = x[mask_included]
    y_filtered = y[mask_included]
    z_filtered = np.full_like(x_filtered, idx * thickness)  # Coordenada Z com base na camada atual

    # Amostrar pontos para reduzir a densidade (opcional, para gráficos menos densos)
    total_points = len(x_filtered)
    sampled_indices = np.random.choice(total_points, size=int(total_points * sampling_factor), replace=False)

    # Obter coordenadas amostradas
    x_sampled = x_filtered[sampled_indices]
    y_sampled = y_filtered[sampled_indices]
    z_sampled = z_filtered[sampled_indices]

    # Plotar os pontos 3D com a cor baseada no valor de intensidade e colormap 'viridis'
    ax.scatter(x_sampled, y_sampled, z_sampled, 
               c=plt.cm.viridis(radon_img_filtered[sampled_indices]),  # Colormap 'viridis'
               marker='o', alpha=0.3, s=20)  # Ajuste o tamanho das bolinhas com s=20 e opacidade com alpha=0.3

# Configurações do gráfico 3D
ax.set_title("Reconstrução 3D com Redução de Ruído e Sem Borda")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z (mm)")
plt.show()

print("Processamento concluído!")
