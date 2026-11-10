SELECT
    c.nome,
    c.estado,
    COUNT(DISTINCT pe.id) AS total_pedidos,
    ROUND(SUM(i.quantidade * i.preco_unitario), 2) AS total_gasto
FROM clientes c
JOIN pedidos pe ON pe.cliente_id = c.id
JOIN itens_pedido i ON i.pedido_id = pe.id
WHERE pe.status = 'entregue'
GROUP BY c.id, c.nome, c.estado
ORDER BY total_gasto DESC
LIMIT 10;