# Trabalho de Faculdade: Processamento de Imagens com Python

Este projeto implementa e demonstra três técnicas de processamento de imagens utilizando Python e bibliotecas populares como OpenCV, Scikit-image, NumPy e Matplotlib. Os algoritmos abordados são:

1.  **Filtros de Frequência**
2.  **Segmentação Watershed**
3.  **Crescimento de Regiões**

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
/trabalho_faculdade_python
|-- filtros_frequencia_python/
|   |-- __init__.py
|   |-- filtros_frequencia.py       # Código principal do algoritmo
|   |-- imagens_exemplo/            # Imagens de entrada para este tópico
|   |   |-- camera_original.png
|   |   |-- moon_original.png
|   |   `-- text_original.png
|   |-- referencias/                # Materiais de referência teórica
|   |   `-- kaggle_skimage_tutorial.md
|   `-- resultados_imagens/         # Imagens geradas pelo algoritmo
|
|-- segmentacao_watershed_python/
|   |-- __init__.py
|   |-- segmentacao_watershed.py    # Código principal do algoritmo
|   |-- imagens_exemplo/
|   |   |-- chelsea_original.png
|   |   `-- coins_original.png
|   |-- referencias/
|   |   `-- skimage_watershed_tutorial.md
|   `-- resultados_imagens/
|
|-- crescimento_regioes_python/
|   |-- __init__.py
|   |-- crescimento_regioes.py      # Código principal do algoritmo
|   |-- imagens_exemplo/
|   |   |-- astronaut_original.png
|   |   |-- horse_original.png
|   |   `-- text_original.png
|   |-- referencias/
|   |   `-- medium_region_growing_tutorial.md
|   `-- resultados_imagens/
|
|-- obter_imagens_teste.py          # Script inicial para obter imagens (pode não ser mais necessário)
|-- requirements.txt                # Dependências Python do projeto
|-- todo_python.md                  # Checklist de tarefas (interno)
`-- README.md                       # Este arquivo
```

## Como Executar os Códigos

### Pré-requisitos

- Python 3.11 ou superior.
- As bibliotecas listadas no arquivo `requirements.txt`.

### Instalação das Dependências

Navegue até a pasta raiz do projeto (`/trabalho_faculdade_python`) e execute o seguinte comando no terminal para instalar as dependências:

```bash
pip install -r requirements.txt
```

### Executando os Scripts Individuais

Cada algoritmo possui um script Python principal que pode ser executado independentemente. Para executar um algoritmo específico, navegue até a pasta do respectivo módulo e execute o script Python. Por exemplo, para executar o algoritmo de filtros de frequência:

```bash
cd filtros_frequencia_python
python filtros_frequencia.py
```

Os resultados (imagens processadas e figuras de comparação) serão salvos na subpasta `resultados_imagens/` dentro de cada módulo.

## Relatório Final

O relatório final disponibilizado contém: 

*   Explicações teóricas sobre cada um dos algoritmos.
*   Os códigos Python implementados.
*   Resultados visuais da aplicação dos algoritmos em imagens de exemplo.
*   Conclusões sobre cada técnica.

## Imagens de Exemplo

As imagens de exemplo utilizadas para testar os algoritmos estão localizadas nas subpastas `imagens_exemplo/` de cada módulo correspondente.

## Referências

Os materiais de referência teórica utilizados para cada tópico estão nas subpastas `referencias/` de cada módulo.

