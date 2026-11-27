
INSERT INTO warehouse.fact_order_items (
    order_id,
    order_item_id,
    customer_key,
    product_key,
    seller_key,
    order_date_key,
    shipping_limit_date,
    price,
    freight_value
)
SELECT
    oi.order_id,
    oi.order_item_id,
    dc.customer_key,
    dp.product_key,
    ds.seller_key,
    TO_CHAR(o.order_purchase_timestamp, 'YYYYMMDD')::INTEGER,
    oi.shipping_limit_date,
    oi.price,
    oi.freight_value
FROM staging.stg_order_items oi
INNER JOIN staging.stg_orders o
    ON oi.order_id = o.order_id
INNER JOIN warehouse.dim_customer dc
    ON o.customer_id = dc.customer_id
INNER JOIN warehouse.dim_product dp
    ON oi.product_id = dp.product_id
INNER JOIN warehouse.dim_seller ds
    ON oi.seller_id = ds.seller_id
INNER JOIN warehouse.dim_date dd
    ON o.order_purchase_timestamp::DATE = dd.full_date
ON CONFLICT (order_id, order_item_id)
DO UPDATE SET
    customer_key = EXCLUDED.customer_key,
    product_key = EXCLUDED.product_key,
    seller_key = EXCLUDED.seller_key,
    order_date_key = EXCLUDED.order_date_key,
    shipping_limit_date = EXCLUDED.shipping_limit_date,
    price = EXCLUDED.price,
    freight_value = EXCLUDED.freight_value;
