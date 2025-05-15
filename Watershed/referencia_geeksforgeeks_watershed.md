# Segmentação de Imagem com o Algoritmo Watershed – OpenCV Python - GeeksforGeeks

A segmentação de imagem é uma tarefa fundamental em visão computacional que envolve a divisão de uma imagem em regiões significativas e semanticamente homogêneas. O objetivo é simplificar a representação da imagem ou torná-la mais significativa para análises posteriores. Esses segmentos geralmente correspondem a objetos ou regiões de interesse dentro da imagem.

## Algoritmo Watershed

O Algoritmo Watershed é uma técnica clássica de segmentação de imagem baseada no conceito de transformação de linhas de separação (watershed). O processo de segmentação leva em consideração a semelhança com os pixels adjacentes como referência importante para conectar pixels com posições espaciais e valores de cinza semelhantes.

### **Quando usar o algoritmo Watershed?**

O Algoritmo Watershed é utilizado na segmentação de imagens com objetos tocando ou sobrepostos. Ele se destaca em cenários com formas de objetos irregulares, necessidades de segmentação baseada em gradientes e quando é possível usar segmentação guiada por marcadores.

### Funcionamento do Algoritmo Watershed

O algoritmo divide uma imagem em segmentos usando informações topográficas. Ele trata a imagem como uma superfície topográfica, identificando bacias hidrográficas com base na intensidade dos pixels. Mínimos locais são marcados como pontos de partida, e uma "inundação" com cores preenche as bacias até alcançar os limites dos objetos. A segmentação resultante atribui cores únicas às regiões, auxiliando no reconhecimento de objetos e análise de imagem.

O processo completo pode ser resumido nos seguintes passos:

* **Colocação de marcadores:** O primeiro passo é posicionar marcadores nos mínimos locais da imagem. Esses marcadores servem como pontos de partida para o processo de inundação.
* **Inundação:** O algoritmo inunda a imagem com cores diferentes, começando pelos marcadores. À medida que as cores se espalham, preenchem as bacias até atingir os limites dos objetos ou regiões.
* **Formação das bacias hidrográficas:** Com a propagação das cores, as bacias são gradualmente preenchidas, criando a segmentação da imagem. As regiões resultantes recebem cores únicas para identificação.
* **Identificação de contornos:** O algoritmo utiliza os limites entre as regiões coloridas para identificar os objetos ou áreas na imagem. A segmentação obtida pode ser usada para reconhecimento de objetos, análise de imagem e extração de características.

## Implementando o algoritmo Watershed com OpenCV

OpenCV (Open Source Computer Vision Library) é uma biblioteca de código aberto voltada para visão computacional e aprendizado de máquina. Contém centenas de algoritmos para detecção de objetos, reconhecimento facial, processamento de imagem e aprendizado de máquina.

### Etapas da implementação com OpenCV:

#### Importando as bibliotecas necessárias

```python
import cv2
import numpy as np
from IPython.display import Image, display
from matplotlib import pyplot as plt
```

#### Carregando a imagem

Definimos uma função `imshow` para exibir a imagem processada. O código carrega a imagem "coin.jpg".

```python
# Exibir imagem
def imshow(img, ax=None):
    if ax is None:
        ret, encoded = cv2.imencode(".jpg", img)
        display(Image(encoded))
    else:
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax.axis("off")

# Carregando a imagem
img = cv2.imread("Coins.png")

# Exibindo
imshow(img)
```

#### Convertendo para imagem em tons de cinza

A imagem é convertida para escala de cinza usando `cvtColor` do OpenCV. A imagem em tons de cinza é armazenada na variável `gray`.

#### Implementando a limiarização (thresholding)

A limiarização transforma uma imagem em tons de cinza em uma imagem binária, essencial para distinguir objetos do fundo.

Quando usamos `cv2.THRESH_BINARY_INV` junto com `cv2.THRESH_OTSU`, aplicamos o método de binarização de Otsu. Ele determina automaticamente um limiar ideal que maximiza a variância entre dois grupos de pixels, separando eficazmente fundo e objeto.

> **Binarização de Otsu**
>
> O método de Otsu é utilizado para separar o primeiro plano e o fundo de uma imagem em duas classes distintas. Ele calcula o limiar ideal que maximiza a variância entre essas classes. É simples, eficiente e bastante usado em análise de documentos, reconhecimento de objetos e imagens médicas.

```python
# Processamento de threshold
ret, bin_img = cv2.threshold(
    gray,
    0,
    255,
    cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)
imshow(bin_img)
```

#### **Passo 4: Remoção de ruído**

Para limpar os contornos dos objetos, remove-se ruído usando processamento morfológico com gradiente.

> **Processamento morfológico por gradiente**
>
> O gradiente morfológico realça as bordas dos objetos, sendo calculado pela subtração da erosão da imagem da sua dilatação. A erosão reduz regiões claras, enquanto a dilatação as expande. O resultado destaca as bordas e pode ser usado para detectar objetos e fazer segmentações.

```python
# Remoção de ruído
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
bin_img = cv2.morphologyEx(
    bin_img,
    cv2.MORPH_OPEN,
    kernel,
    iterations=2
)
imshow(bin_img)
```

#### Detectando o fundo preto e o primeiro plano da imagem

O próximo passo é isolar a área preta (fundo) da imagem. Se a parte branca estiver bem preenchida, ela será considerada como a área de interesse...

---

**Fonte:**
[GeeksForGeeks – Image Segmentation with Watershed Algorithm – OpenCV Python](https://www.geeksforgeeks.org/image-segmentation-with-watershed-algorithm-opencv-python/)
