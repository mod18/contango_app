--De-dupes fct_closing_quotes_raw
INSERT INTO fct_closing_quotes_daily
SELECT
    date,
    ticker_name,
    ticker_contract,
    closing_price,
    source,
    MAX(retrieved_ts) AS retrieved_ts
FROM fct_closing_quotes_raw
WHERE
    date = '{date}'
    AND closing_price IS NOT NULL
GROUP BY 1, 2, 3, 4, 5
;