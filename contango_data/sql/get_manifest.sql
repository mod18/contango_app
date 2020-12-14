SELECT
       t.ticker_name,
       t.ticker_type,
       t.exchange,
       t.num_contracts,
       t.leverage_ratio
FROM main_ticker t
INNER JOIN main_category c
    ON c.id = t.category_id
WHERE c.category_name='{category_name}'
;
