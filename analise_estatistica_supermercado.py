# Análise simples dos preços e descontos do supermercado

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# Lê a base que está na mesma pasta deste arquivo
dados = pd.read_csv("base_supermercado.csv")

# Calcula média, mediana e desvio padrão do preço normal por categoria
resumo = dados.groupby("Categoria")["Preco_Normal"].agg(
    ["mean", "median", "std"]
)
resumo.columns = ["media", "mediana", "desvio_padrao"]

print("Média e mediana do preço normal por categoria:")
print(resumo.round(2))

# Compara a média e a mediana dentro de cada categoria
print("\nCategorias em que a média é maior que a mediana:")
print(resumo[resumo["media"] > resumo["mediana"]].index.tolist())

print("\nCategorias em que a média é menor ou igual à mediana:")
print(resumo[resumo["media"] <= resumo["mediana"]].index.tolist())

# Descobre qual categoria tem o maior desvio padrão
categoria_maior_desvio = resumo["desvio_padrao"].idxmax()
print("\nCategoria com maior desvio padrão:", categoria_maior_desvio)

# Faz o boxplot dos preços dessa categoria
precos = dados[dados["Categoria"] == categoria_maior_desvio]["Preco_Normal"]
q1 = precos.quantile(0.25)
q3 = precos.quantile(0.75)
intervalo = q3 - q1
limite_inferior = q1 - 1.5 * intervalo
limite_superior = q3 + 1.5 * intervalo

outliers = precos[(precos < limite_inferior) | (precos > limite_superior)]
print("Quantidade de outliers no boxplot:", len(outliers))

sns.boxplot(x=precos)
plt.title("Preço normal na categoria " + categoria_maior_desvio)
plt.xlabel("Preço normal")
plt.tight_layout()
plt.savefig("boxplot_preco_normal.png")
plt.close()

# Faz o gráfico de barras da média de desconto por categoria
desconto_categoria = dados.groupby("Categoria")["Desconto"].mean().sort_values()
desconto_categoria.plot(kind="bar", color="teal")
plt.title("Desconto médio por categoria")
plt.xlabel("Categoria")
plt.ylabel("Desconto médio")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("desconto_medio_por_categoria.png")
plt.close()

# Agrupa por categoria e marca para fazer o mapa interativo
mapa = dados.groupby(["Categoria", "Marca"]).agg(
    desconto_medio=("Desconto", "mean"),
    quantidade=("Desconto", "count"),
).reset_index()

grafico_mapa = px.treemap(
    mapa,
    path=["Categoria", "Marca"],
    values="quantidade",
    color="desconto_medio",
    title="Desconto médio por categoria e marca",
)
grafico_mapa.write_html("mapa_categoria_marca.html")

print("\nGráficos salvos na mesma pasta do código.")
