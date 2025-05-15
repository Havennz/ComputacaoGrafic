-- Crescimento de Regiões (Simulação Simplificada)
-- Este código demonstra uma simulação do algoritmo de Crescimento de Regiões
-- para segmentar uma imagem simples representada como uma matriz de pixels.

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

-- Função para imprimir a imagem de rótulos (matriz) no console
local function imprimir_rotulos(rotulos, titulo)
    print(titulo or "Rótulos da Imagem Segmentada:")
    for y = 1, #rotulos do
        local linha = ""
        for x = 1, #rotulos[y] do
            linha = linha .. string.format("%2d ", rotulos[y][x] or 0) -- Mostrar 0 se não rotulado
        end
        print(linha)
    end
    print("\n")
end

-- Função para imprimir a imagem de intensidade (matriz) no console
local function imprimir_intensidade(imagem, titulo)
    print(titulo or "Imagem de Intensidade:")
    for y = 1, #imagem do
        local linha = ""
        for x = 1, #imagem[y] do
            linha = linha .. string.format("%3d ", imagem[y][x])
        end
        print(linha)
    end
    print("\n")
end

-- Função para obter vizinhos de 8 conexões (incluindo diagonais)
local function obter_vizinhos_8_conexoes(ponto, largura, altura)
    local vizinhos = {}
    local x, y = ponto.x, ponto.y
    for dy = -1, 1 do
        for dx = -1, 1 do
            if not (dx == 0 and dy == 0) then -- Não incluir o próprio ponto
                local vizinho_x, vizinho_y = x + dx, y + dy
                if vizinho_x >= 1 and vizinho_x <= largura and vizinho_y >= 1 and vizinho_y <= altura then
                    table.insert(vizinhos, {x = vizinho_x, y = vizinho_y})
                end
            end
        end
    end
    return vizinhos
end

-- Algoritmo de Crescimento de Regiões Simplificado
local function crescimento_regioes(imagem_original, sementes, limiar_similaridade)
    local altura = #imagem_original
    local largura = #imagem_original[1]
    local rotulos = criar_imagem(largura, altura, 0) -- 0 significa não rotulado
    local proximo_rotulo = 1

    for _, semente_info in ipairs(sementes) do
        local ponto_semente = semente_info.ponto
        
        -- Se a semente já foi rotulada (parte de outra região), ignora
        if rotulos[ponto_semente.y][ponto_semente.x] ~= 0 then
            goto continue_semente -- Usando goto para pular para a próxima iteração do loop externo
        end

        local rotulo_atual = proximo_rotulo
        proximo_rotulo = proximo_rotulo + 1
        
        rotulos[ponto_semente.y][ponto_semente.x] = rotulo_atual
        local fila_processamento = {ponto_semente}
        local valor_medio_regiao = imagem_original[ponto_semente.y][ponto_semente.x]
        local contador_pixels_regiao = 1

        local indice_fila = 1
        while indice_fila <= #fila_processamento do
            local pixel_atual = fila_processamento[indice_fila]
            indice_fila = indice_fila + 1

            local vizinhos = obter_vizinhos_8_conexoes(pixel_atual, largura, altura)
            for _, vizinho in ipairs(vizinhos) do
                if rotulos[vizinho.y][vizinho.x] == 0 then -- Se o vizinho não foi rotulado
                    local valor_vizinho = imagem_original[vizinho.y][vizinho.x]
                    -- Critério de similaridade: diferença absoluta em relação ao valor da semente inicial
                    -- Ou poderia ser em relação à média da região atual (mais adaptativo)
                    if math.abs(valor_vizinho - imagem_original[ponto_semente.y][ponto_semente.x]) <= limiar_similaridade then
                    -- Alternativa: if math.abs(valor_vizinho - valor_medio_regiao) <= limiar_similaridade then
                        rotulos[vizinho.y][vizinho.x] = rotulo_atual
                        table.insert(fila_processamento, vizinho)
                        -- Atualizar média da região (se for usar critério adaptativo)
                        -- valor_medio_regiao = (valor_medio_regiao * contador_pixels_regiao + valor_vizinho) / (contador_pixels_regiao + 1)
                        -- contador_pixels_regiao = contador_pixels_regiao + 1
                    end
                end
            end
        end
        ::continue_semente::
    end

    return rotulos
end

-- --- Exemplo de Uso ---

-- Imagem de exemplo (valores de intensidade)
local imagem_exemplo = {
    {10, 10, 10, 80, 80, 80},
    {10, 12, 11, 78, 82, 79},
    {11,  9, 13, 81, 77, 83},
    {90, 92, 91, 20, 22, 21},
    {88, 93, 89, 19, 23, 20},
    {91, 90, 92, 22, 21, 18}
}
imprimir_intensidade(imagem_exemplo, "Imagem Original para Crescimento de Regiões")

-- Pontos de semente (escolhidos manualmente ou por algum critério)
-- Cada semente tem um ponto {x, y}
local sementes_exemplo = {
    {ponto = {x = 2, y = 2}}, -- Semente para a região de baixa intensidade (aprox. 10)
    {ponto = {x = 5, y = 2}}, -- Semente para a região de média intensidade (aprox. 80)
    {ponto = {x = 2, y = 5}}, -- Semente para a região de alta intensidade (aprox. 90)
    {ponto = {x = 5, y = 5}}  -- Semente para a região de baixa intensidade (aprox. 20)
}

-- Limiar de similaridade (diferença máxima de intensidade para um pixel ser incluído na região)
local limiar = 10

local rotulos_resultado = crescimento_regioes(imagem_exemplo, sementes_exemplo, limiar)
imprimir_rotulos(rotulos_resultado, "Imagem Segmentada com Crescimento de Regiões")

print("Nota: A ordem das sementes e o critério de similaridade podem influenciar o resultado.")
print("Esta é uma implementação simplificada. Algoritmos mais robustos podem usar critérios mais complexos e lidar com sobreposição de regiões.")

