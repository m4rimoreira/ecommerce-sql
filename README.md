# 🛒 E-commerce Analytics com SQL

Análise de vendas de um e-commerce fictício usando SQL (SQLite) e Python.

## 🎯 Objetivo

Responder 5 perguntas de negócio a partir de um banco relacional: faturamento por categoria, top clientes, ticket médio por estado, taxa de recompra e evolução mensal.

## 🛠 Tecnologias

SQL · SQLite · Python · Pandas · Matplotlib

## 🗂 Estrutura

- queries/ — 5 consultas SQL organizadas
- outputs/ — gráficos e resultados
- criar_banco.py — gera o banco fictício
- analise_sql.py — executa as consultas e gera gráficos

## ▶️ Como executar

1. pip install -r requirements.txt
2. python criar_banco.py
3. python analise_sql.py

## 🔍 Consultas

| Arquivo | Técnicas SQL |
|---|---|
| 01_faturamento_categoria | JOIN, GROUP BY, COUNT(DISTINCT) |
| 02_top_clientes | JOIN, ORDER BY, LIMIT |
| 03_ticket_medio_estado | SUM / COUNT(DISTINCT) |
| 04_taxa_recompra | CTE (WITH), CASE WHEN |
| 05_faturamento_mensal | strftime, GROUP BY |

## 💡 Insights (Dados Fictícios)

- **Eletrônicos** lidera com **R$ 1.602.061** (~66% do total)
- **Faturamento total:** R$ 2.412.550
- **Cliente top:** Carla Oliveira — R$ 41.931

## 👩‍💻 Autora

Mariana Moreira — [GitHub](https://github.com/m4rimoreira) · [LinkedIn](https://www.linkedin.com/in/mariana-moreira-9b2b2b2aa)