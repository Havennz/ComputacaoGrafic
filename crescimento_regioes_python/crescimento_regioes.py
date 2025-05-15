import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import skimage.io
from skimage import img_as_ubyte, color

class Stack():
    def __init__(self):
        self.item = []
        self.obj = []

    def push(self, item, obj):
        self.item.append(item)
        self.obj.append(obj)

    def pop(self):
        if not self.isEmpty():
            return self.item.pop(), self.obj.pop()

    def isEmpty(self):
        return len(self.item) == 0

    def length(self):
        return len(self.item)

def aplicar_crescimento_regioes(caminho_imagem_entrada, caminho_imagem_saida_base, semente_coords, limiar_similaridade=10):
    """
    Aplica o algoritmo de crescimento de regiões a uma imagem a partir de uma semente.

    Args:
        caminho_imagem_entrada (str): Caminho para a imagem de entrada.
        caminho_imagem_saida_base (str): Caminho base para salvar as imagens de saída (sem extensão).
        semente_coords (tuple): Coordenadas (linha, coluna) do pixel semente.
        limiar_similaridade (int): Diferença máxima de intensidade para um pixel ser incluído na região.
    """
    print(f"[DEBUG] Iniciando aplicar_crescimento_regioes para: {caminho_imagem_entrada} com semente {semente_coords}")
    diretorio_saida = os.path.dirname(caminho_imagem_saida_base)
    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)
        print(f"[DEBUG] Diretório de saída criado: {diretorio_saida}")

    img_original_color = skimage.io.imread(caminho_imagem_entrada)
    if img_original_color is None:
        print(f"[ERRO] Erro ao carregar a imagem: {caminho_imagem_entrada}")
        return
    print(f"[DEBUG] Imagem carregada: {caminho_imagem_entrada}, shape: {img_original_color.shape}")

    if len(img_original_color.shape) == 3:
        img_gray = color.rgb2gray(img_original_color)
    else:
        img_gray = img_original_color
    
    img_gray_ubyte = img_as_ubyte(img_gray)
    print(f"[DEBUG] Imagem convertida para escala de cinza ubyte, shape: {img_gray_ubyte.shape}")

    altura, largura = img_gray_ubyte.shape
    img_segmentada = np.zeros_like(img_gray_ubyte)
    visitados = np.zeros_like(img_gray_ubyte, dtype=bool)

    pilha = Stack()
    
    semente_linha, semente_coluna = semente_coords
    if not (0 <= semente_linha < altura and 0 <= semente_coluna < largura):
        print(f"[ERRO] Coordenadas da semente {semente_coords} fora dos limites da imagem ({altura}x{largura}).")
        return

    valor_semente = img_gray_ubyte[semente_linha, semente_coluna]
    pilha.push((semente_linha, semente_coluna), valor_semente) # O segundo argumento 'obj' não é usado como no artigo original, mas mantido para estrutura da Stack
    visitados[semente_linha, semente_coluna] = True
    img_segmentada[semente_linha, semente_coluna] = 255 # Marca a região com branco

    print(f"[DEBUG] Semente inicial: ({semente_linha}, {semente_coluna}), Valor: {valor_semente}")

    while not pilha.isEmpty():
        (x, y), _ = pilha.pop()
        
        # Vizinhos de 8 conexões
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x + dx, y + dy

                if 0 <= nx < altura and 0 <= ny < largura and not visitados[nx, ny]:
                    visitados[nx, ny] = True
                    valor_vizinho = img_gray_ubyte[nx, ny]
                    if abs(int(valor_vizinho) - int(valor_semente)) <= limiar_similaridade: # Compara com o valor da semente original
                    # Ou poderia ser comparado com a média da região atual, ou com o pixel vizinho que o adicionou
                        img_segmentada[nx, ny] = 255
                        pilha.push((nx, ny), valor_vizinho)
    
    print("[DEBUG] Processo de crescimento de região concluído.")

    # Salvar imagens
    img_original_com_semente = img_original_color.copy()
    if len(img_original_com_semente.shape) == 2: # Se for cinza, converte para color para marcar a semente
        img_original_com_semente = color.gray2rgb(img_as_ubyte(img_original_com_semente))
    
    cv2.circle(img_original_com_semente, (semente_coluna, semente_linha), radius=5, color=(255,0,0), thickness=-1) # Vermelho para semente

    skimage.io.imsave(f"{caminho_imagem_saida_base}_original.png", img_as_ubyte(img_original_color))
    skimage.io.imsave(f"{caminho_imagem_saida_base}_original_com_semente.png", img_as_ubyte(img_original_com_semente))
    skimage.io.imsave(f"{caminho_imagem_saida_base}_segmentada.png", img_segmentada)
    print(f"[DEBUG] Imagens de crescimento de regiões salvas em {diretorio_saida}")

    # Plotar e salvar figura combinada
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    ax = axes.ravel()

    ax[0].imshow(img_original_color, cmap='gray' if len(img_original_color.shape)==2 else None)
    ax[0].set_title("Imagem Original")
    ax[0].axis("off")

    ax[1].imshow(img_original_com_semente)
    ax[1].set_title(f"Semente em ({semente_linha},{semente_coluna})")
    ax[1].axis("off")

    ax[2].imshow(img_segmentada, cmap="gray")
    ax[2].set_title(f"Região Crescida (Limiar: {limiar_similaridade})")
    ax[2].axis("off")

    fig.tight_layout()
    path_figura_comparacao = f"{caminho_imagem_saida_base}_comparacao_crescimento.png"
    plt.savefig(path_figura_comparacao)
    plt.close(fig)
    print(f"[DEBUG] Figura de comparação de Crescimento de Regiões salva em {path_figura_comparacao}")
    print(f"[DEBUG] Finalizando aplicar_crescimento_regioes para: {caminho_imagem_entrada}")

if __name__ == "__main__":
    base_path_projeto = "/home/ubuntu/trabalho_faculdade_python"
    path_modulo_crescimento = os.path.join(base_path_projeto, "crescimento_regioes_python")
    path_imagens_exemplos = os.path.join(path_modulo_crescimento, "imagens_exemplo")
    path_resultados = os.path.join(path_modulo_crescimento, "resultados_imagens")

    if not os.path.exists(path_resultados):
        os.makedirs(path_resultados)

    imagens_e_sementes = {
        "astronaut_original.png": [(200, 200), (100,100)], # Exemplo: semente no rosto, semente no capacete
        "horse_original.png": [(150, 200), (50,50)],       # Exemplo: semente no corpo do cavalo, semente no fundo
        "text_original.png": [(80, 100), (20,20)]          # Exemplo: semente em uma letra, semente no fundo
    }
    
    limiar_teste = 20 # Limiar de similaridade para teste

    for nome_img, lista_sementes in imagens_e_sementes.items():
        caminho_img = os.path.join(path_imagens_exemplos, nome_img)
        if os.path.exists(caminho_img):
            for i, semente in enumerate(lista_sementes):
                print(f"\n[MAIN] Processando {nome_img} com semente {semente} (limiar: {limiar_teste})")
                nome_base_saida = os.path.splitext(nome_img)[0] + f"_semente{i+1}_limiar{limiar_teste}"
                aplicar_crescimento_regioes(caminho_img, os.path.join(path_resultados, nome_base_saida), semente, limiar_teste)
        else:
            print(f"[ERRO] Imagem de exemplo {nome_img} não encontrada em: {caminho_img}")

    print("\nProcessamento de crescimento de regiões concluído.")

