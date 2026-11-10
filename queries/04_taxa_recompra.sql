WITH compras_por_cliente AS (
    SELECT
        c.id,
        c.nome,
        COUNT(DISTINCT pe.id) AS qtd_pedidos
    FROM clientes c
    JOIN pedidos pe ON pe.cliente_id = c.id
    WHERE pe.status = 'entregue'
    GROUP BY c.id, c.nome
)
SELECT
    nome,
    qtd_pedidos,
    CASE WHEN qtd_pedidos >= 3 THEN 'Recorrente'
         WHEN qtd_pedidos = 2 THEN 'Ocasional'
         ELSE 'Unico' END AS perfil
FROM compras_por_cliente
ORDER BY qtd_pedidos DESC
LIMIT 20;