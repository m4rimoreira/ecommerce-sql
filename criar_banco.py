"""
Cria o banco SQLite 'ecommerce.db' com dados fictícios de e-commerce.
Execute UMA VEZ antes de rodar analise_sql.py.
"""

import sqlite3
import random
from datetime import datetime, timedelta
import os

os.makedirs("data", exist_ok=True)
random.seed(42)  

conn = sqlite3.connect("data/ecommerce.db")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS itens_pedido;

CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT,
    estado TEXT,
    data_cadastro DATE
);

CREATE TABLE produtos (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    categoria TEXT,
    preco REAL
);

CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER,
    data_pedido DATE,
    status TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE itens_pedido (
    id INTEGER PRIMARY KEY,
    pedido_id INTEGER,
    produto_id INTEGER,
    quantidade INTEGER,
    preco_unitario REAL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);
""")

estados = ["SP", "RJ", "MG", "RS", "PR", "BA", "SC", "PE", "CE", "DF"]
nomes = ["Ana", "Bruno", "Carla", "Diego", "Eduarda", "Felipe", "Gabriela",
         "Henrique", "Isabela", "João", "Larissa", "Marcos", "Natália",
         "Otávio", "Paula", "Rafael", "Sofia", "Thiago", "Vanessa", "Wagner"]
sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Lima", "Pereira",
              "Costa", "Ferreira", "Almeida", "Rodrigues"]

clientes = []
for i in range(1, 201):
    nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
    email = f"cliente{i}@email.com"
    estado = random.choice(estados)
    data_cadastro = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
    clientes.append((i, nome, email, estado, data_cadastro.date()))

cur.executemany("INSERT INTO clientes VALUES (?, ?, ?, ?, ?)", clientes)


categorias = {
    "Eletrônicos": (200, 3000),
    "Roupas": (50, 300),
    "Livros": (30, 150),
    "Casa": (80, 800),
    "Esportes": (100, 1000),
}

produtos = []
for i in range(1, 51):
    cat = random.choice(list(categorias.keys()))
    preco_min, preco_max = categorias[cat]
    nome = f"Produto {i} - {cat}"
    preco = round(random.uniform(preco_min, preco_max), 2)
    produtos.append((i, nome, cat, preco))

cur.executemany("INSERT INTO produtos VALUES (?, ?, ?, ?)", produtos)


pedidos = []
itens = []
item_id = 1
for pedido_id in range(1, 801):
    cliente_id = random.randint(1, 200)

    data_pedido = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 364))
    status = random.choices(
        ["entregue", "cancelado", "pendente"],
        weights=[0.85, 0.08, 0.07]
    )[0]
    pedidos.append((pedido_id, cliente_id, data_pedido.date(), status))


    for _ in range(random.randint(1, 4)):
        produto_id = random.randint(1, 50)
        preco_unit = next(p[3] for p in produtos if p[0] == produto_id)
        quantidade = random.randint(1, 3)
        itens.append((item_id, pedido_id, produto_id, quantidade, preco_unit))
        item_id += 1

cur.executemany("INSERT INTO pedidos VALUES (?, ?, ?, ?)", pedidos)
cur.executemany("INSERT INTO itens_pedido VALUES (?, ?, ?, ?, ?)", itens)

conn.commit()


cur.execute("SELECT COUNT(*) FROM clientes")
print(f"✔ Clientes: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM produtos")
print(f"✔ Produtos: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pedidos")
print(f"✔ Pedidos: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM itens_pedido")
print(f"✔ Itens: {cur.fetchone()[0]}")

conn.close()
print("\n✅ Banco criado em data/ecommerce.db")