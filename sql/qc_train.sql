SELECT
    l.lot_qty,
    q.qc_qty,
    i.item_type,
    i.item_qc_type,
    q.qc_type,
    NVL(w.work_order_qty, 0) AS work_order_qty,
    NVL(w.work_worker, 'NONE') AS work_worker,
    TO_CHAR(q.qc_date, 'MM') AS qc_month,
    TO_CHAR(q.qc_date, 'D') AS qc_weekday,
    NVL(
    TO_NUMBER(
        REGEXP_SUBSTR(q.qc_wmsg, '위험점수=([0-9]+)', 1, 1, NULL, 1)
    ),
    0
) AS inspection_risk_score,
CASE
    WHEN TO_CHAR(q.qc_date, 'MM') IN ('06', '07', '08') THEN 1
    ELSE 0
END AS summer_flag,
CASE
	WHEN TO_CHAR(q.qc_date, 'MM') IN ('12', '01', '02') THEN 1
	ELSE 0
END AS winter_flag,
CASE
	WHEN ((l.lot_qty - q.qc_pass_qty) / NULLIF(l.lot_qty, 0)) * 100 >= 3 THEN 'HIGH'
	WHEN ((l.lot_qty - q.qc_pass_qty) / NULLIF(l.lot_qty, 0)) * 100 >= 1 THEN 'MEDIUM'
	ELSE 'LOW'
END AS risk_level
FROM
qc q
JOIN lot l
    ON
q.qc_lot = l.lot_id
JOIN item i
    ON
l.lot_item = i.item_id
LEFT JOIN WORK w
    ON
l.lot_work = w.work_id
WHERE
q.qc_usage = 'Y'
AND l.lot_qty > 0
AND q.qc_pass_qty IS NOT NULL
