SELECT
    strftime('%Y-%m', pe.data_pedido) AS mes,
    ROUND(SUM(i.quantidade * i.preco_unitario), 2) AS faturamento
FROM pedidos pe
JOIN itens_pedido i ON i.pedido_id = pe.id
WHERE pe.status = 'entregue'
GROUP BY mes
ORDER BY mes;