SELECT
    c.estado,
    COUNT(DISTINCT pe.id) AS pedidos,
    ROUND(SUM(i.quantidade * i.preco_unitario) / COUNT(DISTINCT pe.id), 2) AS ticket_medio
FROM clientes c
JOIN pedidos pe ON pe.cliente_id = c.id
JOIN itens_pedido i ON i.pedido_id = pe.id
WHERE pe.status = 'entregue'
GROUP BY c.estado
ORDER BY ticket_medio DESC;