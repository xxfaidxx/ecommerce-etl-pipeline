INSERT INTO warehouse.fact_order_payments (
    order_id,
    payment_sequential,
    customer_key,
    payment_type,
    payment_installments,
    payment_value,
    is_zero_payment
)
SELECT
    p.order_id,
    p.payment_sequential,
    dc.customer_key,
    p.payment_type,
    p.payment_installments,
    p.payment_value,
    p.payment_value = 0
FROM staging.stg_order_payments p
INNER JOIN staging.stg_orders o
    ON p.order_id = o.order_id
INNER JOIN warehouse.dim_customer dc
    ON o.customer_id = dc.customer_id
ON CONFLICT (order_id, payment_sequential)
DO UPDATE SET
    customer_key = EXCLUDED.customer_key,
    payment_type = EXCLUDED.payment_type,
    payment_installments = EXCLUDED.payment_installments,
    payment_value = EXCLUDED.payment_value,
    is_zero_payment = EXCLUDED.is_zero_payment;