-- Updates fct_futures_daily
WITH futures_prices AS (
    --Get current date closing futures prices
    SELECT
           id,
           date,
           ticker_name,
           ticker_contract,
           closing_price
    FROM fct_closing_quotes_daily
    WHERE
        date = '{date}'
        AND ticker_contract IS NOT NULL
),
prices_denormalized AS (
    --Denormalize prices
    SELECT
        c1.id AS id,
        c1.date,
        t.id AS ticker_id,
        c1.closing_price AS closing_price_1,
        c1.id AS c1_quote_id,
        c2.closing_price AS closing_price_2,
        c2.id AS c2_quote_id,
        c3.closing_price AS closing_price_3,
        c3.id AS c3_quote_id
    FROM main_ticker t
    LEFT OUTER JOIN futures_prices c1
        ON c1.ticker_name = t.ticker_name
        AND c1.ticker_contract = 1
    LEFT OUTER JOIN futures_prices c2
        ON c2.ticker_name = t.ticker_name
        AND c2.ticker_contract = 2
    LEFT OUTER JOIN futures_prices c3
        ON c3.ticker_name = t.ticker_name
        AND c3.ticker_contract = 3
    WHERE
        t.ticker_type = 'Future'
),
daily_calc AS (
    SELECT
        id,
        date,
        ticker_id,
        CASE
            WHEN closing_price_2 > closing_price_1 THEN 'Yes'
            WHEN closing_price_2 < closing_price_1 THEN 'No'
        END AS contango,
        ROUND(closing_price_2 - closing_price_1, 4) AS front_contango,
        closing_price_1,
        id AS c1_quote_id,
        closing_price_2,
        c2_quote_id,
        closing_price_3,
        c3_quote_id
    FROM prices_denormalized
)
INSERT INTO fct_futures_daily
(id,
date,
ticker_id,
contango,
front_contango,
closing_price_1,
c1_quote_id,
closing_price_2,
c2_quote_id,
closing_price_3,
c3_quote_id)
SELECT
    id,
    date,
    ticker_id,
    contango,
    front_contango,
    closing_price_1,
    c1_quote_id,
    closing_price_2,
    c2_quote_id,
    closing_price_3,
    c3_quote_id
FROM daily_calc
;