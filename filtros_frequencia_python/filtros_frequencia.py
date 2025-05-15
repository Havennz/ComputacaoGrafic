import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import skimage.io
from skimage import img_as_ubyte, color, exposure

def aplicar_filtros_frequencia(caminho_imagem_entrada, caminho_imagem_saida_base):
    """
    Aplica filtros de frequência (passa-baixa e passa-alta Gaussiano) a uma imagem.

    Args:
        caminho_imagem_entrada (str): Caminho para a imagem de entrada.
        caminho_imagem_saida_base (str): Caminho base para salvar as imagens de saída (sem extensão).
    """
    print(f"[DEBUG] Iniciando aplicar_filtros_frequencia para: {caminho_imagem_entrada}")
    diretorio_saida = os.path.dirname(caminho_imagem_saida_base)
    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)
        print(f"[DEBUG] Diretório de saída criado: {diretorio_saida}")

    img = skimage.io.imread(caminho_imagem_entrada)
    if img is None:
        print(f"[ERRO] Erro ao carregar a imagem: {caminho_imagem_entrada}")
        return
    print(f"[DEBUG] Imagem carregada: {caminho_imagem_entrada}, shape: {img.shape}")

    if len(img.shape) == 3:
        img_gray = color.rgb2gray(img)
    else:
        img_gray = img
    
    img_gray_ubyte = img_as_ubyte(img_gray)
    print(f"[DEBUG] Imagem convertida para escala de cinza ubyte, shape: {img_gray_ubyte.shape}")

    # Transformada de Fourier
    dft = cv2.dft(np.float32(img_gray), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    magnitude_spectrum_original = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]) + 1e-6) # Adicionado 1e-6 para evitar log(0)

    rows, cols = img_gray.shape
    crow, ccol = rows // 2, cols // 2

    # --- Filtro Passa-Baixa Gaussiano ---
    print("[DEBUG] Aplicando Filtro Passa-Baixa Gaussiano")
    # Criar máscara para filtro passa-baixa (exemplo com D0 = 30)
    D0_low = 30
    mask_low = np.zeros((rows, cols, 2), np.float32)
    for r in range(rows):
        for c in range(cols):
            D = np.sqrt((r - crow)**2 + (c - ccol)**2)
            mask_low[r, c, 0] = np.exp(-(D**2) / (2 * D0_low**2))
            mask_low[r, c, 1] = np.exp(-(D**2) / (2 * D0_low**2))

    fshift_low = dft_shift * mask_low
    magnitude_spectrum_low = 20 * np.log(cv2.magnitude(fshift_low[:, :, 0], fshift_low[:, :, 1]) + 1e-6)
    f_ishift_low = np.fft.ifftshift(fshift_low)
    img_back_low = cv2.idft(f_ishift_low, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)
    img_back_low_norm = cv2.normalize(img_back_low, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # --- Filtro Passa-Alta Gaussiano ---
    print("[DEBUG] Aplicando Filtro Passa-Alta Gaussiano")
    # Criar máscara para filtro passa-alta (exemplo com D0 = 30)
    D0_high = 30
    mask_high = np.zeros((rows, cols, 2), np.float32)
    for r in range(rows):
        for c in range(cols):
            D = np.sqrt((r - crow)**2 + (c - ccol)**2)
            mask_high[r, c, 0] = 1 - np.exp(-(D**2) / (2 * D0_high**2))
            mask_high[r, c, 1] = 1 - np.exp(-(D**2) / (2 * D0_high**2))
    
    fshift_high = dft_shift * mask_high
    magnitude_spectrum_high = 20 * np.log(cv2.magnitude(fshift_high[:, :, 0], fshift_high[:, :, 1]) + 1e-6)
    f_ishift_high = np.fft.ifftshift(fshift_high)
    img_back_high = cv2.idft(f_ishift_high, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)
    img_back_high_norm = cv2.normalize(img_back_high, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Salvar imagens
    print("[DEBUG] Iniciando salvamento de imagens.")
    skimage.io.imsave(f"{caminho_imagem_saida_base}_original_gray.png", img_gray_ubyte)
    skimage.io.imsave(f"{caminho_imagem_saida_base}_magnitude_spectrum_original.png", cv2.normalize(magnitude_spectrum_original, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8))
    skimage.io.imsave(f"{caminho_imagem_saida_base}_passa_baixa_gaussiano.png", img_back_low_norm)
    skimage.io.imsave(f"{caminho_imagem_saida_base}_magnitude_spectrum_low.png", cv2.normalize(magnitude_spectrum_low, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8))
    skimage.io.imsave(f"{caminho_imagem_saida_base}_passa_alta_gaussiano.png", img_back_high_norm)
    skimage.io.imsave(f"{caminho_imagem_saida_base}_magnitude_spectrum_high.png", cv2.normalize(magnitude_spectrum_high, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8))
    print(f"[DEBUG] Imagens de filtros de frequência salvas em {diretorio_saida}")

    # Plotar e salvar figura combinada
    print("[DEBUG] Iniciando plotagem e salvamento da figura combinada.")
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    ax = axes.ravel()

    ax[0].imshow(img_gray_ubyte, cmap="gray")
    ax[0].set_title("Imagem Original Cinza")
    ax[1].imshow(magnitude_spectrum_original, cmap="gray")
    ax[1].set_title("Espectro de Magnitude Original")
    ax[2].axis("off") # Espaço vazio

    ax[3].imshow(img_back_low_norm, cmap="gray")
    ax[3].set_title("Filtro Passa-Baixa Gaussiano (D0=30)")
    ax[4].imshow(img_back_high_norm, cmap="gray")
    ax[4].set_title("Filtro Passa-Alta Gaussiano (D0=30)")
    ax[5].axis("off") # Espaço vazio
    
    # Adicionar espectros filtrados se desejado, ou mais imagens
    # ax[2].imshow(magnitude_spectrum_low, cmap="gray")
    # ax[2].set_title("Espectro Pós Passa-Baixa")
    # ax[5].imshow(magnitude_spectrum_high, cmap="gray")
    # ax[5].set_title("Espectro Pós Passa-Alta")

    for a_plot in ax:
        if a_plot.images: # Só desliga o eixo se houver imagem
            # Mantendo eixos para espectros e imagens para melhor visualização
            a_plot.set_xticks([])
            a_plot.set_yticks([])
        else:
            a_plot.axis("off")
    fig.tight_layout()
    path_figura_comparacao = f"{caminho_imagem_saida_base}_comparacao_filtros_frequencia.png"
    plt.savefig(path_figura_comparacao)
    plt.close(fig)
    print(f"[DEBUG] Figura de comparação de Filtros de Frequência salva em {path_figura_comparacao}")
    print(f"[DEBUG] Finalizando aplicar_filtros_frequencia para: {caminho_imagem_entrada}")

if __name__ == "__main__":
    base_path_projeto = "/home/ubuntu/trabalho_faculdade_python"
    path_modulo_freq = os.path.join(base_path_projeto, "filtros_frequencia_python")
    path_imagens_exemplos_freq = os.path.join(path_modulo_freq, "imagens_exemplo") # Usar pasta de imagens do módulo
    path_resultados_freq = os.path.join(path_modulo_freq, "resultados_imagens")

    if not os.path.exists(path_resultados_freq):
        os.makedirs(path_resultados_freq)

    # Imagem de exemplo: camera (da skimage, salva anteriormente)
    img_camera_path = os.path.join(path_imagens_exemplos_freq, "camera_original.png")
    if os.path.exists(img_camera_path):
        print(f"[MAIN] Processando camera: {img_camera_path}")
        aplicar_filtros_frequencia(img_camera_path, os.path.join(path_resultados_freq, "camera_filtros"))
    else:
        print(f"[ERRO] Imagem de exemplo camera não encontrada em: {img_camera_path}")

    # Imagem de exemplo: text (da skimage, salva anteriormente)
    img_text_path = os.path.join(path_imagens_exemplos_freq, "text_original.png")
    if os.path.exists(img_text_path):
        print(f"[MAIN] Processando text: {img_text_path}")
        aplicar_filtros_frequencia(img_text_path, os.path.join(path_resultados_freq, "text_filtros"))
    else:
        print(f"[ERRO] Imagem de exemplo text não encontrada em: {img_text_path}")

    print("Processamento de filtros de frequência concluído.")

