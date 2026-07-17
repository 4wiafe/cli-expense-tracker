SELECT category,
    COALESCE(SUM(amount), 0) as total
FROM expenses
GROUP BY category