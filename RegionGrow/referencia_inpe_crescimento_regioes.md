# Segmentação de Imagens - Spring (INPE)

**Segmentação de Imagens**  
  
_O que é a segmentação de Imagens?_  
  

*   A classificação estatística é o procedimento convencional de análise digital de imagens. Constitui um processo de análise de pixels de forma isolada. Esta abordagem apresenta a limitação da análise pontual ser baseada unicamente em atributos espectrais. Para superar estas limitações, propõe-se o uso de segmentação de imagem, anterior à fase de classificação, onde se extraem os objetos relevantes para a aplicação desejada.
*   Neste processo, divide-se a imagem em regiões que devem corresponder às áreas de interesse da aplicação. Entende-se por regiões um conjunto de "pixels" contíguos, que se espalham bidirecionalmente e que apresentam uniformidade.
*   A divisão em porções consiste basicamente em um processo de crescimento de regiões, de detecção de bordas ou de detecção de bacias.

_O que é crescimento de regiões?_  
  

*   É uma técnica de agrupamento de dados, na qual somente as regiões adjacentes, espacialmente, podem ser agrupadas.
*   Inicialmente, este processo de segmentação rotula cada "pixel" como uma região distinta. Calcula-se um critério de similaridade para cada par de região adjacente espacialmente. O critério de similaridade baseia-se em um teste de hipótese estatístico que testa a média entre as regiões. A seguir, divide-se a imagem em um conjunto de sub-imagens e então realiza-se a união entre elas, segundo um limiar de agregação definido.
*   Para a união de duas regiões A e B vizinhas, deve-se adotar o seguinte critério:
    *   A e B são similares (teste das médias);
    *   a similaridade satisfaz o limiar estabelecido;
    *   A e B são mutuamente próximas (dentre os vizinhos de A, B é a mais próxima, e dentre os vizinhos de B, A é a mais próxima).
*   Caso as regiões A e B satisfaçam estes critérios, estas regiões são agregadas, caso contrário o sistema reinicia o processo de teste de agregação.

_O que é detecção de bacias?_  
  

*   A classificação por detecção de bacias é feita sobre uma imagem resultante da extração de bordas.
*   A extração de bordas é realizada por um algoritmo de detecção de bordas, ou seja pelo filtro de Sobel. Este algoritmo considera os gradientes de nível de cinza da imagem original, para gerar uma imagem gradiente ou imagem de intensidade de borda.
*   O algoritmo calcula um limiar para a perseguição de bordas. Quando ele encontra um "pixel" com valor superior ao limiar estabelecido, tem-se início o processo de perseguição da borda. Observa-se a vizinhança para identificar o próximo "pixel" de maior valor de nível digital e segue-se nesta direção até que se encontre outra borda ou a fronteira da imagem. Deste processo gera-se uma imagem binária com os valores de 1 referentes às bordas e 0, a regiões de não-bordas.
*   A imagem binária será rotulada de modo que as porções da imagem com valores 0 constituirão regiões limitadas pelos valores 1 da imagem, constituindo a imagem rotulada.
*   O procedimento de segmentação por detecção de bacias pressupõe uma representação topográfica para a imagem, ou seja, para uma dada imagem gradiente, o valor de nível digital de cada "pixel" equivale a um valor de elevação naquele ponto. A imagem equivaleria a uma superfície topográfica com feições de relevo ou uma região com bacias de diferentes profundidades.
*   O crescimento de uma região equivaleria à imersão da superfície topográfica em um lago. Define-se um altura inicial (nível digital) para o preenchimento das bacias (limiar). A "água" preencherá progressivamente as diferentes bacias da imagem até um limiar definido pela topografia (valor de nível digital). Ao alcançar o limite, define-se uma barreira entre duas regiões. O processo de preenchimento continua em outra direção até atingir um novo limite topográfico, definindo-se mais uma barreira, e assim sucessivamente até que todas as barreiras tenham sido definidas.
*   O resultado é uma imagem rotulada, cada região apresentando um rótulo (valor de nível digital), que devem ser classificadas por classificadores de região.

_Como classificar imagens segmentadas?_  
  

*   O classificador Isoseg é o algoritmo disponível no Spring para classificar regiões de uma imagem segmentada. É um algoritmo de agrupamento de dados não-supervisionado, aplicado sobre o conjunto de regiões, que por sua vez são caracterizadas por seus atributos estatísticos de média e matriz de covariância, e também pela área.
*   Um algoritmo de "clustering" não assume nenhum conhecimento prévio da distribuição de densidade de probabilidade dos temas, como ocorre no algoritmo de máxima verossimilhança. É uma técnica para classificação que procura agrupar regiões, a partir de uma medida de similaridade entre elas. A medida de similaridade utilizada consiste na distância de Mahalanobis entre a classe e as regiões candidatas a relação de pertinência com esta classe.
*   O Isoseg utiliza os atributos estatísticos das regiões: a matriz de covariância e o vetor de média, para estimar o valor central de cada classe. Este algoritmo resume-se em três etapas, descritas a seguir.
    *   (1ª) **Definição do limiar**: o usuário define um limiar de aceitação, dado em percentagem. Este limiar por sua vez define uma distância de Mahalanobis, de forma que todas regiões pertencentes a uma dada classe estão distantes da classe por uma distância inferior a esta. Quanto maior o limiar, maior esta distância e consequentemente maior será o número de classes detectadas pelo algoritmo.
    *   (2ª) **Detecção das classes**: as regiões são ordenadas em ordem decrescente de área e inicia-se o procedimento para agrupá-las em classes. Serão tomados como parâmetros estatísticos de uma classe (média e matriz de covariância), os parâmetros estatísticos da região de maior área que ainda não tenha sido associada a classe alguma. Em seguida, associa-se a esta classe todas regiões cuja distância de Mahalanobis for inferior a distância definida pelo limiar de aceitação. Assim, a primeira classe terá como parâmetros estatísticos aquelas regiões com maior área. As classes seguintes terão parâmetros estatísticos de média das regiões de maior área, que não tenham sido associada a nenhuma das classes previamente detectadas. Esta fase repete-se até que todas regiões tenham sido associadas a alguma classe.
    *   (3ª) **Competição entre classes**: as regiões são reclassificadas, considerando-se os novos parâmetros estatísticos das classes, definidos na etapa anterior.
*   A fase 2 consiste basicamente na detecção de classes, sendo um processo seqüencial que pode favorecer as classes que são detectadas em primeiro lugar. Com vista a eliminar este favorecimento", procede-se a "competição entre classes. Esta competição consiste em reclassificar todas as regiões. O parâmetro estatístico (média de cada classe é então recalculado. O processo repete-se até que a média das classes não se altere (convergência).
*   Ao término, todas regiões estarão associadas a uma classe definida pelo algoritmo. O usuário deverá então associar estas classes (denominadas temas, no Spring) às classes por ele definidas no banco de dados, na opção Arquivo-Esquema Conceitual, descrito no capítulo 5, volume1.
*   Portanto o usuário deve seguir os seguintes passos para gerar uma classificação a partir de uma imagem segmentada, observe que os passos de 2 a 9 foram descritos anteriormente:
    *   **Criar uma imagem segmentada** - gerar uma imagem, separada em regiões com base na análise dos níveis de cinza.
    *   **Criar o arquivo de Contexto** - este arquivo armazena quais as bandas farão parte do processo...

Fonte: [http://www.dpi.inpe.br/spring/portugues/tutorial/segmentacao.html](http://www.dpi.inpe.br/spring/portugues/tutorial/segmentacao.html)

