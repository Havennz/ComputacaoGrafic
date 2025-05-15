import cv2
import numpy as np
from skimage.segmentation import watershed
# from skimage.feature import peak_local_max # Not directly used in the final version of watershed logic
# from skimage.morphology import disk, opening, closing # Not directly used
from skimage.filters import sobel
from scipy import ndimage as ndi
from matplotlib import pyplot as plt
import os
import skimage.io
from skimage import img_as_ubyte, color, exposure

def aplicar_segmentacao_watershed(caminho_imagem_entrada, caminho_imagem_saida_base, usar_distancia=True):
    """
    Aplica a segmentação watershed a uma imagem.

    Args:
        caminho_imagem_entrada (str): Caminho para a imagem de entrada.
        caminho_imagem_saida_base (str): Caminho base para salvar as imagens de saída (sem extensão).
        usar_distancia (bool): Se True, usa a transformada de distância para encontrar marcadores (OpenCV style).
                             Se False, usa gradiente e mínimos regionais (Scikit-image style).
    """
    print(f"[DEBUG] Iniciando aplicar_segmentacao_watershed para: {caminho_imagem_entrada}")
    diretorio_saida = os.path.dirname(caminho_imagem_saida_base)
    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)
        print(f"[DEBUG] Diretório de saída criado: {diretorio_saida}")

    img_color_original = skimage.io.imread(caminho_imagem_entrada)
    if img_color_original is None:
        print(f"[ERRO] Erro ao carregar a imagem: {caminho_imagem_entrada}")
        return
    print(f"[DEBUG] Imagem carregada: {caminho_imagem_entrada}, shape: {img_color_original.shape}")

    img_para_watershed_cv = img_color_original.copy()

    if len(img_color_original.shape) == 3:
        img_gray = color.rgb2gray(img_color_original)
    else:
        img_gray = img_color_original

    img_ubyte = img_as_ubyte(img_gray)
    print(f"[DEBUG] Imagem convertida para ubyte, shape: {img_ubyte.shape}")

    if usar_distancia:
        print("[DEBUG] Usando método de transformada de distância (OpenCV)")
        _, thresh = cv2.threshold(img_ubyte, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = np.ones((3,3),np.uint8)
        opening_img = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
        sure_bg = cv2.dilate(opening_img,kernel,iterations=3)
        dist_transform = cv2.distanceTransform(opening_img,cv2.DIST_L2,5)
        _, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg,sure_fg)
        _, markers_cv = cv2.connectedComponents(sure_fg)
        markers_cv = markers_cv + 1 
        markers_cv[unknown==255] = 0 
        
        if len(img_para_watershed_cv.shape) == 2: 
            img_para_watershed_cv = color.gray2rgb(img_as_ubyte(img_para_watershed_cv))
        
        cv2.watershed(img_para_watershed_cv, markers_cv)
        img_resultado_watershed = img_para_watershed_cv.copy()
        img_resultado_watershed[markers_cv == -1] = [255,0,0] 

        etapa_intermediaria_titulo = "Transformada de Distância"
        etapa_intermediaria_img_plot = dist_transform
        marcadores_plot = cv2.normalize(markers_cv.astype(np.float32), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        marcadores_titulo = "Marcadores (OpenCV)"
        print("[DEBUG] Método OpenCV concluído.")
    else:
        print("[DEBUG] Usando método de gradiente (Scikit-image)")
        gradient = sobel(img_ubyte)
        markers_sk_bool = np.zeros_like(img_ubyte, dtype=bool)
        markers_sk_bool[img_ubyte < np.percentile(img_ubyte, 20)] = True 
        markers_sk_bool[img_ubyte > np.percentile(img_ubyte, 80)] = True 
        markers_sk_labeled, _ = ndi.label(markers_sk_bool)
        labels_ws = watershed(gradient, markers_sk_labeled, mask=img_ubyte > 0) 
        img_resultado_watershed = color.label2rgb(labels_ws, image=img_color_original, bg_label=0, kind="overlay")
        etapa_intermediaria_titulo = "Magnitude do Gradiente (Sobel)"
        etapa_intermediaria_img_plot = gradient
        marcadores_plot = color.label2rgb(markers_sk_labeled, image=img_color_original, bg_label=0)
        marcadores_titulo = "Marcadores (Scikit-image)"
        print("[DEBUG] Método Scikit-image concluído.")

    print("[DEBUG] Iniciando salvamento de imagens intermediárias e resultado.")
    skimage.io.imsave(f"{caminho_imagem_saida_base}_original.png", img_as_ubyte(img_color_original))
    
    if etapa_intermediaria_img_plot.dtype == np.float32 or etapa_intermediaria_img_plot.dtype == np.float64:
        print(f"[DEBUG] Normalizando etapa_intermediaria_img_plot (tipo: {etapa_intermediaria_img_plot.dtype}, min: {etapa_intermediaria_img_plot.min()}, max: {etapa_intermediaria_img_plot.max()})")
        etapa_intermediaria_img_plot_save = cv2.normalize(etapa_intermediaria_img_plot, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    else:
        etapa_intermediaria_img_plot_save = img_as_ubyte(etapa_intermediaria_img_plot)
    skimage.io.imsave(f"{caminho_imagem_saida_base}_etapa_intermediaria.png", etapa_intermediaria_img_plot_save)
    
    skimage.io.imsave(f"{caminho_imagem_saida_base}_marcadores.png", img_as_ubyte(marcadores_plot))
    skimage.io.imsave(f"{caminho_imagem_saida_base}_segmentada_watershed.png", img_as_ubyte(img_resultado_watershed))
    print(f"[DEBUG] Imagens individuais salvas em {diretorio_saida}")

    # Corrigido: f-string para o print, usando aspas simples externas
    print(f'Segmentação Watershed (método: {"Distância" if usar_distancia else "Gradiente"}) aplicada e imagens salvas em {diretorio_saida}')

    print("[DEBUG] Iniciando plotagem e salvamento da figura combinada.")
    fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(16, 5), sharex=True, sharey=True)
    ax = axes.ravel()

    ax[0].imshow(img_color_original, cmap=plt.cm.gray if len(img_color_original.shape)==2 else None)
    ax[0].set_title("Imagem Original")
    ax[1].imshow(etapa_intermediaria_img_plot_save, cmap="gray")
    ax[1].set_title(etapa_intermediaria_titulo)
    ax[2].imshow(marcadores_plot, cmap=plt.cm.nipy_spectral if (usar_distancia and marcadores_plot.ndim == 2) else None) 
    ax[2].set_title(marcadores_titulo)
    ax[3].imshow(img_resultado_watershed)
    ax[3].set_title("Segmentação Watershed")

    for a_plot in ax:
        a_plot.axis("off")

    fig.tight_layout()
    # Corrigido: f-string para o path_figura_comparacao, usando aspas simples externas
    path_figura_comparacao = f'{caminho_imagem_saida_base}_comparacao_watershed_{"dist" if usar_distancia else "grad"}.png'
    plt.savefig(path_figura_comparacao)
    plt.close(fig)
    print(f"[DEBUG] Figura de comparação Watershed salva em {path_figura_comparacao}")
    print(f"[DEBUG] Finalizando aplicar_segmentacao_watershed para: {caminho_imagem_entrada}")

if __name__ == "__main__":
    base_path_projeto = "/home/ubuntu/trabalho_faculdade_python"
    path_modulo_watershed = os.path.join(base_path_projeto, "segmentacao_watershed_python")
    path_imagens_exemplo = os.path.join(path_modulo_watershed, "imagens_exemplo")
    path_resultados = os.path.join(path_modulo_watershed, "resultados_imagens")

    if not os.path.exists(path_resultados):
        os.makedirs(path_resultados)

    img_coins_original_path = os.path.join(path_imagens_exemplo, "coins_original.png")
    print(f"[MAIN] Processando coins: {img_coins_original_path}")
    aplicar_segmentacao_watershed(img_coins_original_path, os.path.join(path_resultados, "coins"), usar_distancia=True)
    
    img_chelsea_original_path = os.path.join(path_imagens_exemplo, "chelsea_original.png")
    print(f"[MAIN] Processando chelsea: {img_chelsea_original_path}")
    aplicar_segmentacao_watershed(img_chelsea_original_path, os.path.join(path_resultados, "chelsea"), usar_distancia=True)
    
    print(f"[MAIN] Processando chelsea (método gradiente): {img_chelsea_original_path}")
    aplicar_segmentacao_watershed(img_chelsea_original_path, os.path.join(path_resultados, "chelsea_grad"), usar_distancia=False)

    print("Processamento de segmentação watershed concluído.")

