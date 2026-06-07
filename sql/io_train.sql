SELECT
    io.io_type,
    io.io_reason,
    io.io_qty,
    l.lot_qty,
    l.lot_fqty,
    i.item_type,
    i.item_unit_price,
    s.stock_prev_qty,
    s.stock_avail_qty,
    s.stock_reserve_qty,
    ROUND((s.stock_reserve_qty / NULLIF(s.stock_prev_qty, 0)) * 100, 2) AS reserve_rate,
    TO_CHAR(io.io_date, 'MM') AS io_month,
    TO_CHAR(io.io_date, 'D') AS io_weekday,
    CASE
        WHEN io.io_reason = '폐기' THEN 'HIGH'
        WHEN TRUNC(l.lot_exp) - TRUNC(io.io_date) <= 0 THEN 'HIGH'
        WHEN TRUNC(l.lot_exp) - TRUNC(io.io_date) <= 15 THEN 'WARNING'
        WHEN (s.stock_reserve_qty / NULLIF(s.stock_prev_qty, 0)) * 100 >= 30 THEN 'WARNING'
        ELSE 'LOW'
    END AS risk_level
FROM io io
JOIN lot l
    ON io.io_lot = l.lot_id
JOIN item i
    ON l.lot_item = i.item_id
LEFT JOIN stock s
    ON s.stock_item = i.item_id
WHERE io.io_usage = 'Y'
