-- Filtros de Frequência (Simulação com Filtros Espaciais)
-- Este código demonstra a aplicação de filtros espaciais que simulam
-- efeitos de filtros de frequência (passa-baixa e passa-alta)
-- em uma imagem representada como uma matriz de pixels.

-- Função para criar uma matriz (imagem) preenchida com um valor
local function criar_imagem(largura, altura, valor_padrao)
    local imagem = {}
    for y = 1, altura do
        imagem[y] = {}
        for x = 1, largura do
            imagem[y][x] = valor_padrao or 0
        end
    end
    return imagem
end

-- Função para imprimir a imagem (matriz) no console
local function imprimir_imagem(imagem, titulo)
    print(titulo or "Imagem:")
    for y = 1, #imagem do
        local linha = ""
        for x = 1, #imagem[y] do
            linha = linha .. string.format("%3d ", imagem[y][x])
        end
        print(linha)
    end
    print("\n")
end

-- Função para aplicar um filtro de média (simulando passa-baixa)
-- Este filtro suaviza a imagem, reduzindo ruído e detalhes finos.
local function filtro_media(imagem_original)
    local altura = #imagem_original
    local largura = #imagem_original[1]
    local imagem_filtrada = criar_imagem(largura, altura)

    for y = 1, altura do
        for x = 1, largura do
            local soma = 0
            local contagem = 0
            -- Kernel 3x3
            for dy = -1, 1 do
                for dx = -1, 1 do
                    local vizinho_y = y + dy
                    local vizinho_x = x + dx
                    if vizinho_y >= 1 and vizinho_y <= altura and vizinho_x >= 1 and vizinho_x <= largura then
                        soma = soma + imagem_original[vizinho_y][vizinho_x]
                        contagem = contagem + 1
                    end
                end
            end
            imagem_filtrada[y][x] = math.floor(soma / contagem)
        end
    end
    return imagem_filtrada
end

-- Função para aplicar um filtro Laplaciano (simulando passa-alta)
-- Este filtro realça bordas e detalhes finos.
-- Kernel Laplaciano comum: [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
local function filtro_laplaciano(imagem_original)
    local altura = #imagem_original
    local largura = #imagem_original[1]
    local imagem_filtrada = criar_imagem(largura, altura)
    
    local kernel = {
        {0,  1, 0},
        {1, -4, 1},
        {0,  1, 0}
    }

    for y = 2, altura - 1 do -- Evita bordas para simplificar
        for x = 2, largura - 1 do
            local soma_ponderada = 0
            for ky = 1, 3 do
                for kx = 1, 3 do
                    soma_ponderada = soma_ponderada + (imagem_original[y + ky - 2][x + kx - 2] * kernel[ky][kx])
                end
            end
            -- O resultado do Laplaciano pode ser negativo. 
            -- Para visualização, pode-se escalar ou tomar o valor absoluto.
            -- Aqui, vamos apenas atribuir, mas em uma aplicação real, o tratamento é importante.
            -- Para manter os valores no range de imagem (ex: 0-255), pode-se subtrair o resultado da original
            -- ou adicionar à original para realce, ou normalizar.
            -- Para este exemplo, vamos apenas mostrar o resultado da convolução.
            -- Um resultado comum é subtrair o laplaciano da imagem original para aguçar:
            -- imagem_filtrada[y][x] = imagem_original[y][x] - soma_ponderada 
            -- Ou apenas o resultado do filtro (que destaca bordas):
            imagem_filtrada[y][x] = soma_ponderada
        end
    end
    return imagem_filtrada
end

-- --- Exemplo de Uso ---

-- Criar uma imagem de exemplo simples
-- Uma região mais clara (100) em um fundo mais escuro (50)
-- com uma borda nítida.
local imagem_teste = criar_imagem(7, 7, 50)
imagem_teste[3][3] = 100; imagem_teste[3][4] = 100; imagem_teste[3][5] = 100;
imagem_teste[4][3] = 100; imagem_teste[4][4] = 100; imagem_teste[4][5] = 100;
imagem_teste[5][3] = 100; imagem_teste[5][4] = 100; imagem_teste[5][5] = 100;


-- Imprimir imagem original
imprimir_imagem(imagem_teste, "Imagem Original")

-- Aplicar filtro de média (simulando passa-baixa)
local imagem_suavizada = filtro_media(imagem_teste)
imprimir_imagem(imagem_suavizada, "Imagem Suavizada (Filtro de Média - Simula Passa-Baixa)")

-- Aplicar filtro Laplaciano (simulando passa-alta)
local imagem_bordas = filtro_laplaciano(imagem_teste)
imprimir_imagem(imagem_bordas, "Imagem com Bordas Realçadas (Filtro Laplaciano - Simula Passa-Alta)")

print("Nota: Os valores de pixel no filtro Laplaciano podem ser negativos ou fora do intervalo [0-255].")
print("Em uma aplicação real, seria necessário normalizar ou processar esses valores para exibição.")

