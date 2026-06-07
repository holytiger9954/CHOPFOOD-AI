SELECT
    inspection_type,
    target_type,
    inspection_result,
    inspection_reason,
    TO_CHAR(inspection_date, 'MM') AS inspection_month,
    TO_CHAR(inspection_date, 'D') AS inspection_weekday,
    CASE
        WHEN risk_score >= 4 THEN 'RISK'
        WHEN risk_score >= 2 THEN 'WARNING'
        ELSE 'NORMAL'
    END AS risk_level
FROM (
    SELECT
        'EQUIPMENT' AS inspection_type,
        'EQUIPMENT' AS target_type,
        e.elog_sdate AS inspection_date,
        e.elog_result AS inspection_result,
        TO_CHAR(e.elog_reason) AS inspection_reason,
        CASE
            WHEN e.elog_reason = 30 THEN 4
            WHEN e.elog_reason = 20 THEN 2
            ELSE 0
        END AS risk_score
    FROM eq_log e
    WHERE e.elog_usage = 'Y'

    UNION ALL

    SELECT
        'GHP' AS inspection_type,
        CASE
            WHEN g.glog_whid IS NOT NULL THEN 'WAREHOUSE'
            WHEN g.glog_wpid IS NOT NULL THEN 'WORKPLACE'
            ELSE 'GHP'
        END AS target_type,
        g.glog_date AS inspection_date,
        g.glog_result AS inspection_result,
        NVL(g.glog_action, '정상') AS inspection_reason,
        CASE
            WHEN g.glog_result = '부적합' THEN 3
            ELSE 0
        END AS risk_score
    FROM ghp_log g
    WHERE g.glog_usage = 'Y'
)