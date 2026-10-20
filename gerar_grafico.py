#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Gráfico 5.7 – MP10 – Evolução das concentrações médias anuais – Baixada Santista e Litoral Norte
================================================================================

Este script gera um gráfico interativo em HTML mostrando a evolução temporal
das concentrações médias anuais de MP₁₀ (material particulado) para estações
de monitoramento na região da Baixada Santista e Litoral Norte de São Paulo.

O gráfico exibe:
- Séries temporais para cada estação (2005-2025)
- Cores e símbolos personalizados para cada localidade
- Dados carregados de um arquivo CSV
- Layout otimizado para visualização e análise

Região de estudo: Cubatão, Santos, São Sebastião e Guarujá
Período de dados: 2005 a 2025 (exibição: 2015-2025)

Autor: Leonardo Rocha
Data: 2026-09-10
Versão: 1.0.0
"""

# =============================================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =============================================================================

from pathlib import Path  # Para manipulação de caminhos de arquivos de forma segura
import pandas as pd       # Para leitura e manipulação de dados em tabelas (DataFrames)
import plotly.graph_objects as go  # Para criação de gráficos interativos


# =============================================================================
# LEITURA DOS DADOS
# =============================================================================

# Define o caminho do arquivo CSV com os dados
# O arquivo deve estar na mesma pasta do script
CSV = Path("Dd_grafico_5_7.csv")

# Lê o arquivo CSV com configurações específicas:
# - sep=None: detecta automaticamente o separador (vírgula, ponto-e-vírgula, etc.)
# - engine="python": usa o parser Python para maior flexibilidade
# - encoding="utf-8-sig": lida com arquivos UTF-8 com BOM (comum em Excel)
df = pd.read_csv(CSV, sep=None, engine="python", encoding="utf-8-sig")


# =============================================================================
# CONFIGURAÇÃO DOS PARÂMETROS
# =============================================================================

# Nome da coluna que contém os nomes das estações de monitoramento
# IMPORTANTE: O nome deve corresponder EXATAMENTE ao que está no CSV
station_col = "estacao"

# Define o período de anos a ser considerado no gráfico
# O range(2005, 2026) gera anos de 2005 a 2025 (inclusive)
# Nota: Embora os dados comecem em 2005, o gráfico exibirá apenas 2015-2025
years = list(range(2015, 2026))


# =============================================================================
# DEFINIÇÃO DAS ESTAÇÕES E ESTILOS PERSONALIZADOS
# =============================================================================

# Lista de estações de monitoramento (Baixada Santista e Litoral Norte)
# A ordem define a ordem de plotagem e aparição na legenda
# (A) = Automática, (M) = Manual
stations = [
    "Cubatão - Centro (A)",                    # Cubatão - Centro - Automática
    "Cubatão - Vale do Mogi (A)",              # Cubatão - Vale do Mogi - Automática
    "Cubatão - Vila Parisi (A)",               # Cubatão - Vila Parisi - Automática
    "Santos (A)",                              # Santos - Automática
    "Santos - Ponta da Praia (A)",             # Santos - Ponta da Praia - Automática
    "São Sebastião (A)",                       # São Sebastião - Automática
    "Guarujá - Vicente de Carvalho (M)",       # Guarujá - Vicente de Carvalho - Manual
]

# Dicionário de estilos personalizados para cada estação
# Cada estação recebe uma combinação específica de cor e símbolo
# Cores escolhidas para serem distintas e visualmente agradáveis
styles = {
    "Cubatão - Centro (A)": ("#E91EAB", "circle"),              # Rosa - Círculo
    "Cubatão - Vale do Mogi (A)": ("#C54B47", "diamond"),       # Vermelho - Losango
    "Cubatão - Vila Parisi (A)": ("#91B64B", "diamond"),        # Verde oliva - Losango
    "Santos (A)": ("#7D5AA5", "triangle-up"),                   # Roxo - Triângulo
    "Santos - Ponta da Praia (A)": ("#45A7C5", "x"),            # Azul ciano - X
    "São Sebastião (A)": ("#F39A45", "circle"),                 # Laranja - Círculo
    "Guarujá - Vicente de Carvalho (M)": ("#B7D18D", "square"), # Verde claro - Quadrado
}


# =============================================================================
# CRIAÇÃO DO GRÁFICO
# =============================================================================

# Inicializa uma figura vazia
fig = go.Figure()

# Itera sobre cada estação na lista predefinida
for station in stations:
    # Busca a linha no DataFrame que corresponde à estação atual
    # astype(str).str.strip() garante que a comparação ignore espaços extras
    match = df.loc[df[station_col].astype(str).str.strip() == station]
    
    # Se a estação não for encontrada no CSV, pula para a próxima
    # Isso evita erros caso o nome da estação no CSV seja diferente
    if match.empty:
        continue
    
    # Pega a primeira linha encontrada (deve ser única)
    row = match.iloc[0]
    
    # Extrai os valores para os anos especificados (2005-2025)
    # Converte para numérico, transformando valores inválidos em NaN
    y = pd.to_numeric(
        row[[str(year) for year in years]], errors="coerce"
    ).tolist()
    
    # Obtém a cor e o símbolo predefinidos para esta estação
    color, symbol = styles[station]
    
    # Adiciona uma série (traço) ao gráfico para esta estação
    fig.add_trace(go.Scatter(
        # Dados do eixo X (anos) e eixo Y (valores de MP₁₀)
        x=years, 
        y=y,
        
        # Modo: linha conectando pontos + marcadores nos pontos
        mode="lines+markers",
        
        # Nome da estação (aparece na legenda e no hover)
        name=station,
        
        # Não conecta pontos onde há valores ausentes (NaN)
        # Se houver anos sem dados, a linha terá interrupções
        connectgaps=False,
        
        # Configuração da linha
        line=dict(
            color=color,          # Cor definida no dicionário styles
            width=3               # Espessura da linha (mais grossa para destaque)
        ),
        
        # Configuração dos marcadores
        marker=dict(
            color=color,          # Cor do marcador (mesma da linha)
            symbol=symbol,        # Símbolo definido no dicionário styles
            size=9                # Tamanho do marcador em pixels
        ),
        
        # Template para o tooltip (informações ao passar o mouse)
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"  # Nome da estação em negrito
            "MP₁₀: %{y:.0f} µg/m³<extra></extra>"  # Valor sem casas decimais
        )
    ))


# =============================================================================
# CONFIGURAÇÃO DO LAYOUT (APARÊNCIA DO GRÁFICO)
# =============================================================================

# Configura o layout do gráfico (títulos, tamanhos, cores, eixos, legenda, etc.)
fig.update_layout(
    # Tema de fundo branco com grade leve
    template="plotly_white",
    
    # Altura da figura em pixels
    height=730,
    
    # Margens ao redor do gráfico (esquerda, direita, topo, base)
    # Margem inferior (155px) para acomodar a legenda horizontal
    margin=dict(l=95, r=45, t=25, b=155),
    
    # Cor de fundo do papel (área externa ao gráfico)
    # Branco - suave e profissional
    paper_bgcolor="#ffffff",
    
    # Cor de fundo da área do gráfico (onde os dados são plotados)
    # Mesma cor para consistência visual
    plot_bgcolor="#ffffff",
    
    # Modo de hover: exibe informações de todas as séries simultaneamente
    # quando o mouse passa sobre um ano específico
    # "x unified" mostra uma linha vertical com todos os valores naquele ano
    hovermode="x unified",
    
    # Configuração do eixo X (horizontal)
    xaxis=dict(
        tickmode="linear",           # Ticks em intervalos regulares
        dtick=1,                     # Intervalo de 1 em 1 ano
        range=[2015, 2025],          # ⚠️ EXIBE APENAS 2015-2025 (mesmo com dados de 2005)
        showgrid=False,              # Sem linhas de grade verticais
        zeroline=False,               # Sem linha no zero do eixo X
        showline=True,                        # Mostra a linha do eixo
        linecolor="#B8B8B8",                   # Cor da linha do eixo (cinza claro)
        ticks="inside"               # Marcadores fora do eixo
    ),
    
    # Configuração do eixo Y (vertical)
    yaxis=dict(
        title="MP₁₀ (µg/m³)",        # Título do eixo com subscrito
        range=[0, 120],              # Limites fixos: 0 a 120 µg/m³
        dtick=20,                    # Intervalo de 20 em 20 µg/m³
        gridcolor="rgba(130,130,130,0.35)",  # Cor das linhas de grade (cinza com 35% opacidade)
        griddash="dash",              # Linhas de grade tracejadas
        showline=True,                        # Mostra a linha do eixo
        linecolor="#B8B8B8",                   # Cor da linha do eixo (cinza claro)
        ticks="outside"               # Marcadores fora do eixo
    ),
    
    # Configuração da legenda
    legend=dict(
        orientation="h",             # Orientação horizontal (em vez de vertical)
        yanchor="top",               # Âncora no topo da legenda
        y=-0.105,                    # Posiciona abaixo do gráfico (valor negativo)
        xanchor="center",            # Centralizado horizontalmente
        x=0.5,                       # Centro do eixo X (50%)
        font=dict(size=12)           # Tamanho da fonte da legenda
    )
)


# =============================================================================
# EXPORTAÇÃO DO GRÁFICO
# =============================================================================

# Salva o gráfico em um arquivo HTML (autônomo, com Plotly embutido)
fig.write_html(
    "index.html",                    # Nome do arquivo de saída
    include_plotlyjs=True,           # Inclui a biblioteca Plotly (não precisa de internet)
    full_html=True,                  # Gera um documento HTML completo
    config={                         # Configurações do gráfico
        "responsive": True,          # Gráfico se adapta ao tamanho da tela
        "displaylogo": False,        # Remove o logo da Plotly da barra de ferramentas
        "scrollZoom": True           # Permite zoom com scroll do mouse
    }
)


# =============================================================================
# MENSAGEM DE CONFIRMAÇÃO
# =============================================================================

# Exibe informações no console sobre o arquivo gerado
print("=" * 70)
print("✅ GRÁFICO GERADO COM SUCESSO!")
print("=" * 70)
print(f"📊 Arquivo: index.html")
print(f"📍 Local: {Path.cwd()}")
print(f"📈 Estações: {len(stations)}")
print(f"📅 Período dos dados: {min(years)} a {max(years)}")
print(f"👁️  Período exibido: 2015 a 2025")
print(f"🎨 Estilos personalizados: {len(styles)} estações configuradas")
print("=" * 70)
print("🌐 Abra o arquivo no navegador para visualizar o gráfico interativo.")