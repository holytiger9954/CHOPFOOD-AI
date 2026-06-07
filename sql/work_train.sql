SELECT
    w.work_order_qty,
    w.work_prev_qty,
    w.work_status,
    w.work_worker,
    w.work_director,
    p.plan_fin_qty,
    p.plan_wp_qty,
    i.item_type,
    TO_CHAR(w.work_date, 'MM') AS work_month,
    TO_CHAR(w.work_date, 'D') AS work_weekday,
    CASE
    WHEN TO_CHAR(w.work_date, 'MM') IN ('06', '07', '08') THEN 1
    ELSE 0
END AS summer_flag,
CASE
    WHEN TO_CHAR(w.work_date, 'MM') IN ('12', '01', '02') THEN 1
    ELSE 0
END AS winter_flag,
CASE
    WHEN w.work_order_qty >= 5000 THEN 2
    WHEN w.work_order_qty >= 3000 THEN 1
    ELSE 0
END AS qty_risk_score,
CASE
	WHEN TO_CHAR(w.work_date, 'MM') = '01' THEN 3
	WHEN TO_CHAR(w.work_date, 'MM') IN ('12', '02') THEN 2
	WHEN TO_CHAR(w.work_date, 'MM') = '07' THEN 2
	WHEN TO_CHAR(w.work_date, 'MM') IN ('06', '08') THEN 1
	ELSE 0
END AS season_risk_score,
CASE
	WHEN TRUNC(w.work_fdate) - TRUNC(w.work_date) >= 2 THEN 'RISK'
	WHEN TRUNC(w.work_fdate) - TRUNC(w.work_date) >= 1 THEN 'DELAY'
	ELSE 'NORMAL'
END AS risk_level
FROM
WORK w
JOIN plan p
    ON
w.work_plan = p.plan_id
JOIN item i
    ON
p.plan_item = i.item_id
WHERE
w.work_usage = 'Y'
AND w.work_order_qty > 0
AND w.work_fdate IS NOT NULL

SELECT
    work_id,
    work_date,
    work_fdate,
    TRUNC(work_fdate) - TRUNC(work_date) AS diff
FROM work
WHERE work_usage='Y'
ORDER BY diff DESC;

SELECT
    p.plan_id,
    p.plan_fin_qty,
    SUM(w.work_order_qty) order_qty,
    SUM(w.work_prev_qty) prod_qty
FROM plan p
LEFT JOIN work w
    ON w.work_plan = p.plan_id
WHERE p.plan_usage = 'Y'
GROUP BY
    p.plan_id,
    p.plan_fin_qty
ORDER BY p.plan_id;

SELECT
    TO_CHAR(w.work_date,'IYYY') || '-W' || TO_CHAR(w.work_date,'IW') week_label,
    COUNT(DISTINCT p.plan_id) plan_cnt,
    SUM(p.plan_fin_qty) plan_qty,
    SUM(w.work_order_qty) order_qty,
    SUM(w.work_prev_qty) prod_qty
FROM work w
JOIN plan p
    ON w.work_plan = p.plan_id
WHERE w.work_usage='Y'
GROUP BY
    TO_CHAR(w.work_date,'IYYY') || '-W' || TO_CHAR(w.work_date,'IW')
ORDER BY week_label;

SELECT
    TO_CHAR(w.work_date,'IYYY') || '-W' || TO_CHAR(w.work_date,'IW') week_label,
    COUNT(*) work_cnt,
    COUNT(DISTINCT p.plan_id) plan_cnt
FROM work w
JOIN plan p
    ON w.work_plan = p.plan_id
WHERE w.work_usage='Y'
GROUP BY
    TO_CHAR(w.work_date,'IYYY') || '-W' || TO_CHAR(w.work_date,'IW')
ORDER BY week_label;

SELECT
    TO_CHAR(work_date,'IYYY') || '-W' || TO_CHAR(work_date,'IW') week_label,
    ROUND(
        SUM(work_prev_qty)
        /
        SUM(work_order_qty)
        * 100
    ,2) achievement_rate
FROM work
WHERE work_usage='Y'
GROUP BY
    TO_CHAR(work_date,'IYYY') || '-W' || TO_CHAR(work_date,'IW')
ORDER BY week_label;
