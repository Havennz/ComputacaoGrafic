# Watershed segmentation - scikit-image

Este arquivo é um registro do conteúdo da página web para referência futura.

**URL:** https://scikit-image.org/docs/0.25.x/auto_examples/segmentation/plot_watershed.html

## Conteúdo Principal (Resumo da Página)

A página da documentação do scikit-image sobre "Watershed segmentation" explica e demonstra o algoritmo watershed para segmentar objetos em uma imagem, especialmente aqueles que estão se tocando.

**Conceitos Chave Apresentados:**

*   **Definição:** O watershed é um algoritmo clássico que trata os valores dos pixels como uma topografia local (elevação).
*   **Funcionamento:** A partir de marcadores definidos pelo usuário (ou mínimos locais), o algoritmo "inunda" bacias até que as bacias de diferentes marcadores se encontrem em "linhas divisórias de águas" (watershed lines).
*   **Aplicação Comum:** Usado para separar objetos sobrepostos.
*   **Pré-processamento:** Frequentemente, calcula-se uma imagem de distância ao fundo. Os máximos dessa distância (mínimos da distância negativa) são usados como marcadores.

**Exemplo de Código Fornecido:**

O exemplo prático demonstra os seguintes passos:

1.  **Geração de Imagem:** Cria uma imagem sintética com dois círculos sobrepostos.
2.  **Cálculo da Distância:** Usa `scipy.ndimage.distance_transform_edt` para calcular a transformada de distância euclidiana da imagem binária. Isso ajuda a identificar os centros dos objetos.
3.  **Identificação de Marcadores:** Utiliza `skimage.feature.peak_local_max` para encontrar os máximos locais na imagem de distância. Esses máximos servirão como marcadores para o algoritmo watershed.
4.  **Rotulagem dos Marcadores:** Usa `scipy.ndimage.label` para atribuir rótulos únicos a cada marcador.
5.  **Aplicação do Watershed:** Aplica a função `skimage.segmentation.watershed` usando a imagem de distância negativa (para que os picos se tornem vales) e os marcadores gerados. A máscara da imagem original é usada para restringir a inundação às áreas dos objetos.
6.  **Visualização:** Mostra a imagem original, a imagem de distâncias e a imagem segmentada com os objetos separados.

**Bibliotecas Utilizadas no Exemplo:**

*   `numpy` para manipulação de arrays.
*   `matplotlib.pyplot` para visualização.
*   `scipy.ndimage` para a transformada de distância e rotulagem.
*   `skimage.segmentation.watershed` para o algoritmo watershed.
*   `skimage.feature.peak_local_max` para encontrar os marcadores.

Este exemplo é uma excelente referência para entender a aplicação prática do algoritmo watershed com scikit-image e como preparar os dados de entrada (especialmente os marcadores) para obter uma boa segmentação.

