--Updates final downstream EFT price table
INSERT INTO fct_etf_daily
(id,
ticker_id,
date,
closing_price)
SELECT
    q.id,
    t.id AS ticker_id,
    q.date,
    q.closing_price
FROM fct_closing_quotes_daily q
INNER JOIN main_ticker t
    ON t.ticker_name = q.ticker_name
WHERE
    q.date = '{date}'
    AND q.ticker_contract IS NULL
;