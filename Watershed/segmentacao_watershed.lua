-- Segmentação Watershed (Simulação Simplificada)
-- Este código demonstra uma simulação conceitual do algoritmo Watershed
-- para segmentar uma imagem simples representada como uma matriz de pixels.
-- Dada a complexidade de uma implementação completa de Watershed em Lua puro
-- sem bibliotecas de processamento de imagem, este exemplo foca na lógica central
-- de "inundação" a partir de marcadores (mínimos locais).

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

-- Função para imprimir a imagem (matriz) de rótulos no console
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

-- Função para encontrar vizinhos de 4 conexões
local function obter_vizinhos(ponto, largura, altura)
    local vizinhos = {}
    local x, y = ponto.x, ponto.y
    if x > 1 then table.insert(vizinhos, {x = x - 1, y = y}) end
    if x < largura then table.insert(vizinhos, {x = x + 1, y = y}) end
    if y > 1 then table.insert(vizinhos, {x = x, y = y - 1}) end
    if y < altura then table.insert(vizinhos, {x = x, y = y + 1}) end
    return vizinhos
end

-- Algoritmo Watershed Simplificado (baseado em inundação a partir de marcadores)
local function watershed_simplificado(imagem_intensidade, marcadores)
    local altura = #imagem_intensidade
    local largura = #imagem_intensidade[1]
    local rotulos = criar_imagem(largura, altura, 0) -- 0 significa não rotulado, -1 para watershed lines (não implementado aqui)
    local fila_processamento = {}

    -- Inicializar fila com pixels marcadores e atribuir rótulos iniciais
    for i, marcador_info in ipairs(marcadores) do
        local p = marcador_info.ponto
        local rotulo = marcador_info.rotulo
        if p.y >= 1 and p.y <= altura and p.x >= 1 and p.x <= largura then
            rotulos[p.y][p.x] = rotulo
            table.insert(fila_processamento, p)
        end
    end

    -- Processo de inundação (similar a uma busca em largura priorizada por intensidade)
    -- Para uma simulação mais simples, vamos processar em ordem de intensidade (pixels de menor intensidade primeiro)
    -- Primeiro, coletamos todos os pixels com suas intensidades
    local pixels_ordenados = {}
    for y = 1, altura do
        for x = 1, largura do
            table.insert(pixels_ordenados, {x=x, y=y, intensidade=imagem_intensidade[y][x]})
        end
    end
    -- Ordenar pixels pela intensidade (simulando a inundação das áreas mais baixas primeiro)
    table.sort(pixels_ordenados, function(a,b) return a.intensidade < b.intensidade end)

    -- Iterar sobre os pixels ordenados
    for _, pixel_atual_info in ipairs(pixels_ordenados) do
        local p_atual = {x = pixel_atual_info.x, y = pixel_atual_info.y}
        
        -- Se o pixel atual já tem um rótulo (por ser um marcador ou já processado), continuamos
        if rotulos[p_atual.y][p_atual.x] ~= 0 then
            -- Poderíamos adicionar lógica para linhas watershed aqui se vizinhos tivessem rótulos diferentes
        else
            -- Verificar vizinhos rotulados
            local vizinhos = obter_vizinhos(p_atual, largura, altura)
            local rotulos_vizinhos = {}
            for _, vizinho in ipairs(vizinhos) do
                if rotulos[vizinho.y][vizinho.x] ~= 0 and rotulos[vizinho.y][vizinho.x] ~= -1 then -- Ignora não rotulados e watersheds
                    table.insert(rotulos_vizinhos, rotulos[vizinho.y][vizinho.x])
                end
            end

            if #rotulos_vizinhos > 0 then
                -- Atribuir o rótulo de um vizinho. Em uma implementação real, regras mais complexas seriam usadas.
                -- Para simplificar, pegamos o primeiro rótulo encontrado ou o de menor valor se houver múltiplos.
                -- Se todos os vizinhos rotulados têm o mesmo rótulo, atribui esse rótulo.
                local rotulo_candidato = rotulos_vizinhos[1]
                local todos_iguais = true
                for i = 2, #rotulos_vizinhos do
                    if rotulos_vizinhos[i] ~= rotulo_candidato then
                        todos_iguais = false
                        -- Aqui seria um ponto de formação de linha watershed (-1)
                        -- Para simplificar, vamos apenas atribuir o primeiro encontrado
                        break
                    end
                end
                if todos_iguais then
                     rotulos[p_atual.y][p_atual.x] = rotulo_candidato
                else
                    -- Simulação de linha watershed (não propagamos rótulo)
                    -- Em uma implementação completa, marcaria como -1 e não adicionaria à fila de expansão
                    -- Para este exemplo, deixamos como 0 ou atribuímos um dos rótulos para evitar complexidade
                    rotulos[p_atual.y][p_atual.x] = rotulo_candidato -- Simplificação
                end
            end
        end
    end

    return rotulos
end

-- --- Exemplo de Uso ---

-- Imagem de intensidade (simulando duas bacias de captação separadas por uma crista)
-- Valores menores são "mais baixos"
local imagem_intensidade_exemplo = {
    {9, 9, 9, 9, 9, 9, 9},
    {9, 2, 1, 2, 9, 3, 9},
    {9, 1, 0, 1, 9, 2, 9}, -- Mínimo local em (3,3) com valor 0
    {9, 2, 1, 2, 9, 1, 9}, -- Mínimo local em (6,4) com valor 1
    {9, 9, 9, 9, 9, 2, 9},
    {9, 9, 9, 9, 9, 9, 9}
}
imprimir_intensidade(imagem_intensidade_exemplo, "Imagem de Intensidade Original")

-- Marcadores (mínimos locais identificados previamente ou definidos pelo usuário)
-- Cada marcador tem um ponto (x,y) e um rótulo único para a região
local marcadores_exemplo = {
    {ponto = {x = 3, y = 3}, rotulo = 1}, -- Bacia 1
    {ponto = {x = 6, y = 4}, rotulo = 2}  -- Bacia 2
}

local rotulos_resultado = watershed_simplificado(imagem_intensidade_exemplo, marcadores_exemplo)
imprimir_rotulos(rotulos_resultado, "Imagem Segmentada com Watershed Simplificado")

print("Nota: Esta é uma simulação altamente simplificada do Watershed.")
print("Uma implementação robusta requer estruturas de dados mais complexas (filas de prioridade), tratamento de platôs, e uma definição clara de linhas watershed.")

