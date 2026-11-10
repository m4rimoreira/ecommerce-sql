SELECT
    p.categoria,
    COUNT(DISTINCT pe.id) AS total_pedidos,
    SUM(i.quantidade) AS total_itens,
    ROUND(SUM(i.quantidade * i.preco_unitario), 2) AS faturamento
FROM itens_pedido i
JOIN pedidos pe ON pe.id = i.pedido_id
JOIN produtos p ON p.id = i.produto_id
WHERE pe.status = 'entregue'
GROUP BY p.categoria
ORDER BY faturamento DESC;