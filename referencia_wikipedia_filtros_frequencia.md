# Filtragem no domínio da frequência – Wikipédia, a enciclopédia livre

Filtros são utilizados em imagens / sons para permitir a alteração dos sinais originais de entrada, onde através da aplicação de técnicas de filtros, torna-se possível gerar novos valores de saída para tais sinais. Imagens são representadas essencialmente no domínio espacial, enquanto que sons são representações feitas do domínio do tempo. Tais sinais podem ser convertidos para o domínio da frequência fazendo-se uso, por exemplo, da Transformada Rápida de Fourier (FFT) e em seguida, aplicando-se filtros para o propósito específico em questão.

A realização da filtragem dos dados no domínio da frequência possibilita a alteração dos dados originais em novas informações de saída com a aplicação de filtros como o Passa Baixa ou Passa Alta, permitindo a remoção de ruídos dos sinais, a suavização dos dados, o aumento do contraste ou até o realce dos detalhes de uma imagem, como as bordas, por exemplo.

## Filtros

A aplicação de filtros em uma imagem digital significa a execução de algum tipo de processamento à mesma com o objetivo de se obter uma imagem resultante mais adequada a um determinado propósito do que a imagem original, com o intuito que ela atenda às necessidades de algum estudo ou análise específicos sobre a imagem. Deve-se enfatizar que saber se o resultado obtido após a filtragem é mais adequado ou não irá depender da interpretação do observador, já que as técnicas de aplicação de filtros em imagens são, de uma forma geral, direcionadas a um determinado problema a ser resolvido.

O uso de filtros na área de processamento de imagens objetiva aumentar sua qualidade, através da remoção ruídos ou imperfeições que podem ser gerados durante os diversos processos pelo qual a imagem pode passar, como a aquisição (processo pelo qual uma imagem do mundo real é transformada em uma imagem digital composta por uma matriz de pixels que determinam sua amostragem e onde cada pixel possui uma gradação tonal determinando sua quantização), a transmissão (através do envio da imagem por correio eletrônico ou através da realização de cópias), além dos processos de compressão da mesma. Outras opções possíveis na utilização de técnicas de filtragem de imagens digitais está na acentuação de determinadas características, como por exemplo, a identificação das bordas da mesma, ou até mesmo em melhorias direcionadas ao seu brilho, foco ou contraste.

## Tipos

A filtragem em uma imagem digital pode ser dividida em dois grupos: filtragem do domínio espacial e filtragem do domínio de frequência. A filtragem no domínio da frequência tem suas técnicas fundamentadas no teorema da convolução e nos trabalhos de Jean-Baptiste Joseph Fourier que postulou que qualquer função periódica pode ser expressa como uma soma de senos ou cossenos de diferentes frequências, cada uma multiplicada por um coeficiente diferente.

### Domínio de Frequência

Em análise de sinais, domínio da frequência designa a análise de funções matemáticas com respeito à frequência, em contraste com a análise do domínio do tempo. Um osciloscópio, por exemplo, é uma ferramenta utilizada para visualizar sinais do mundo real no domínio do tempo. Já um analisador de espectro é uma ferramenta usada para visualizar sinais no domínio da frequência.

Um gráfico no domínio do tempo mostra como um sinal varia ao longo do tempo. Já um gráfico no domínio da frequência mostra quanto do sinal reside em cada faixa de frequência. Uma função pode ser convertida do domínio do tempo para o da frequência através de um operador matemático chamado de transformada integral.

### Filtragem no Domínio da Frequência

Em processamento de imagem, **filtragem no domínio da frequência** de uma imagem consiste em transformar a representação da imagem no espaço para o domínio da frequência, aplicando, por exemplo, a transformada de Fourier na imagem, realizando-se em seguida a filtragem desejada e depois calculando-se a transformada inversa de Fourier para obter o resultado da imagem filtrada. González e Woods definem a filtragem no domínio da frequência como a multiplicação de uma função filtro, definida por H(u,v) pela função F(u,v), que é a transformada de Fourier da imagem que se deseja filtrar. A utilização da transformada de Fourier em imagens facilita alguns processos de definição de filtros, reconhecimento de texturas e compressão de imagens, sendo realizada usualmente em 3 passos:

1.  Cada pixel da imagem denominado f(x,y) é transformado do domínio espacial para o de frequência F(u,v), usando a Transformada de Fourier;
2.  Filtros são aplicados na imagem digital através de técnicas de processamento de imagens;
3.  Em seguida, realiza-se o processo inverso, no qual a imagem modificada no domínio da frequência é transformada para o domínio espacial, utilizando-se a Transformada Inversa de Fourier e gerando uma nova imagem processada g(x,y);

## Exemplos de Filtros

Dessa forma, teoricamente, dada uma imagem digital g(x,y), de tamanho M x N, a equação básica de filtragem no qual estamos interessados tem a seguinte forma.

g(x,y) = IDFT[H(u,v)F(u,v)]

Na qual o símbolo IDFT é a IDFT, F(u,v) é a DFT da imagem de entrada da H(u,v) é uma função filtro (também chamada apenas de filtro ou função de transferência de Filtro) e G(u,v) é imagem filtrada de saída. As funções F, H e G são arranjos de tamanho M x N, o mesmo que a imagem de entrada. O produto H(u,v)F(u,v) é formado utilizando a multiplicação de arranjos matriciais. A função filtro modifica a transformada da imagem de entrada para gerar uma de saída processada G(u,v).

### Exemplo prático

#### Filtro de Passa Baixa

Na primeira imagem temos o Filtro de Passa Baixa, onde o processo consiste em atenuar a alta frequência, como ruído, bordas e transições abruptas de intensidades. Dessa forma a suavização (borramento) é obtida no domínio da frequência isto é: pela filtragem (González e Woods)

*   Figura de um automóvel sem filtro
*   Imagem filtrada com filtro de passa baixa

Obtemos uma imagem “borrada”, ou seja, ocorre uma perda de detalhes que são compostos de altas frequências. Aplicando o inverso deste filtro explicitamos os detalhes perdidos na imagem anterior. A imagem a ser filtrada com Filtro de Passa Baixa atenua (ou elimina) as altas frequências que estão relacionadas com a informação de detalhes da imagem. Este filtro possui o efeito visual de suavização (smoothing) da imagem, uma vez que as altas frequências, que correspondem às transições abruptas, são atenuadas. A suavização tende também, pelas mesmas razões, a minimizar o efeito do ruído em imagens. A filtragem Passa Baixa tem, por outro lado, o efeito indesejado de diminuir a resolução da imagem, provocando assim, um leve borramento, ou seja, diminui a nitidez e a definição da imagem.

Tecnicamente, o filtro Passa Baixa é executado conforme as regras abaixo:

H(u,v) = 1 se D(u,v) <= D0
H(u,v) = 0 se D(u,v) > D0

Onde (u,v) são os pixels no domínio de frequência e D0 é o raio que delimita a área de corte da imagem. Neste filtro, todas as frequências da imagem que estiverem dentro do círculo de raio D0 são mantidas e todas fora do círculo são removidas. O ponto onde ocorre a transição entre H(u,v)=1 e H(u,v)=0 é chamado de frequência de corte.

#### Filtro de Passa Alta

O Filtro Passa Alta, como o próprio nome indica, pode ser entendido como uma operação inversa ao Passa Baixa. O aguçamento de detalhes da imagem pode ser obtido no domínio da frequência pela filtragem...
