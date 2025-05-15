# Trabalho de Faculdade - Processamento de Imagens em Lua

Este repositório contém implementações de algoritmos de processamento de imagens em Lua, desenvolvidos como parte de uma tarefa de faculdade. O projeto aborda três tópicos principais:

1.  **Filtros de Frequência (Simulação com Filtros Espaciais)**
2.  **Segmentação Watershed (Simulação Simplificada)**
3.  **Crescimento de Regiões (Simulação Simplificada)**

## Tópicos Abordados

### 1. Filtros de Frequência

Localizado na pasta `filtros_frequencia`.

*   `filtros_frequencia.lua`: Contém uma simulação de filtros de frequência utilizando filtros espaciais (média para passa-baixa e Laplaciano para passa-alta) em Lua. O código inclui funções para criar e imprimir imagens (representadas como matrizes) e aplicar os filtros.
*   `referencia_wikipedia_filtros_frequencia.md`: Material de referência sobre a teoria de filtragem no domínio da frequência.

### 2. Segmentação Watershed

Localizado na pasta `segmentacao_watershed`.

*   `segmentacao_watershed.lua`: Apresenta uma simulação conceitual e simplificada do algoritmo Watershed. Dada a complexidade de uma implementação completa em Lua puro sem bibliotecas dedicadas, o foco é na lógica de "inundação" a partir de marcadores em uma imagem de intensidade.
*   `referencia_geeksforgeeks_watershed.md`: Documentação teórica e um exemplo de implementação (em Python/OpenCV) do algoritmo Watershed, servindo como base conceitual.

### 3. Crescimento de Regiões

Localizado na pasta `crescimento_regioes`.

*   `crescimento_regioes.lua`: Demonstra uma simulação do algoritmo de Crescimento de Regiões. O código parte de pontos de semente e expande as regiões com base em um critério de similaridade de intensidade.
*   `referencia_inpe_crescimento_regioes.md`: Documentação teórica sobre o algoritmo de crescimento de regiões, extraída de material do INPE.
*   `regiongrow.pdf`: Documento PDF original da UFSC que serve como referência aprofundada sobre o tema.

## Como Executar os Códigos

Para executar os arquivos `.lua`, você precisará de um interpretador Lua instalado em seu sistema.

Por exemplo, para executar o código de filtros de frequência:

```bash
lua filtros_frequencia/filtros_frequencia.lua
```

Os scripts foram desenvolvidos para serem autoexplicativos e imprimirão os resultados das simulações no console.

## Relatório

Um relatório detalhado em formato PDF será gerado, cobrindo a teoria, a implementação, os resultados e as conclusões para cada um dos tópicos. Os rascunhos das seções do relatório serão preparados na pasta `relatorios_individuais`.

## Observações

As implementações em Lua são simulações didáticas e simplificadas dos algoritmos, especialmente devido à ausência de bibliotecas gráficas ou de processamento de imagem avançadas diretamente em Lua padrão para manipulação visual de imagens. O foco está em demonstrar a lógica fundamental de cada técnica usando representações matriciais de imagens.
