# Gráfico 5.7 — MP10

Gráfico interativo em Python + Plotly baseado diretamente no CSV fornecido.

## Fonte

`Dd_Grafico_5_7.csv`

Campo das estações:

```text
estacao
```

Para reproduzir a imagem de referência, o gráfico utiliza as 7 estações apresentadas na legenda e o período 2015–2025.

## Estações

- Cubatão - Centro (A)
- Cubatão - Vale do Mogi (A)
- Cubatão - Vila Parisi (A)
- Santos (A)
- Santos - Ponta da Praia (A)
- São Sebastião (A)
- Guarujá - Vicente de Carvalho (M)

## Arquivos

- `index.html` — gráfico Plotly interativo e autocontido.
- `Dd_Grafico_5_7.csv` — CSV completo fornecido.
- `dados_grafico.csv` — dados das séries apresentadas.
- `gerar_grafico.py` — código Python + Pandas + Plotly.
- `.github/workflows/pages.yml` — publicação automática.
- `.nojekyll`
- `publicar_github.bat`
- `README.md`

## Instalação

```bash
pip install pandas plotly
```

## Gerar

```bash
python gerar_grafico.py
```

## Publicar

```bash
git init
git add .
git commit -m "Adicionar grafico MP10 5.7"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

No GitHub:

**Settings → Pages → Build and deployment → Source → GitHub Actions**

URL:

```text
https://SEU_USUARIO.github.io/SEU_REPOSITORIO/
```

Valores ausentes são mantidos como lacunas no gráfico (`connectgaps=False`).
