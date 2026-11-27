
INSERT INTO warehouse.fact_orders (
    order_id,
    customer_key,
    order_date_key,
    approved_date_key,
    delivered_carrier_date_key,
    delivered_customer_date_key,
    estimated_delivery_date_key,
    order_status,
    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date,
    delivery_days,
    estimated_delivery_days,
    delivery_delay_days,
    is_delivered,
    is_late_delivery
)
SELECT
    o.order_id,
    dc.customer_key,

    TO_CHAR(o.order_purchase_timestamp, 'YYYYMMDD')::INTEGER,
    TO_CHAR(o.order_approved_at, 'YYYYMMDD')::INTEGER,
    TO_CHAR(o.order_delivered_carrier_date, 'YYYYMMDD')::INTEGER,
    TO_CHAR(o.order_delivered_customer_date, 'YYYYMMDD')::INTEGER,
    TO_CHAR(o.order_estimated_delivery_date, 'YYYYMMDD')::INTEGER,

    o.order_status,

    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,

    -- Actual delivery duration in days
    CASE
        WHEN o.order_delivered_customer_date IS NOT NULL
        THEN EXTRACT(EPOCH FROM (
            o.order_delivered_customer_date - o.order_purchase_timestamp
        )) / 86400
    END::NUMERIC(10,4),

    -- Estimated delivery duration in days
    CASE
        WHEN o.order_estimated_delivery_date IS NOT NULL
        THEN EXTRACT(EPOCH FROM (
            o.order_estimated_delivery_date - o.order_purchase_timestamp
        )) / 86400
    END::NUMERIC(10,4),

    -- Delivery delay in days
    CASE
        WHEN o.order_delivered_customer_date IS NOT NULL
         AND o.order_estimated_delivery_date IS NOT NULL
        THEN EXTRACT(EPOCH FROM (
            o.order_delivered_customer_date - o.order_estimated_delivery_date
        )) / 86400
    END::NUMERIC(10,4),

    o.order_status = 'delivered',

    CASE
        WHEN o.order_delivered_customer_date IS NOT NULL
         AND o.order_estimated_delivery_date IS NOT NULL
        THEN o.order_delivered_customer_date > o.order_estimated_delivery_date
        ELSE FALSE
    END

FROM staging.stg_orders o
INNER JOIN warehouse.dim_customer dc
    ON o.customer_id = dc.customer_id

ON CONFLICT (order_id)
DO UPDATE SET
    customer_key = EXCLUDED.customer_key,
    order_date_key = EXCLUDED.order_date_key,
    approved_date_key = EXCLUDED.approved_date_key,
    delivered_carrier_date_key = EXCLUDED.delivered_carrier_date_key,
    delivered_customer_date_key = EXCLUDED.delivered_customer_date_key,
    estimated_delivery_date_key = EXCLUDED.estimated_delivery_date_key,
    order_status = EXCLUDED.order_status,
    order_purchase_timestamp = EXCLUDED.order_purchase_timestamp,
    order_approved_at = EXCLUDED.order_approved_at,
    order_delivered_carrier_date = EXCLUDED.order_delivered_carrier_date,
    order_delivered_customer_date = EXCLUDED.order_delivered_customer_date,
    order_estimated_delivery_date = EXCLUDED.order_estimated_delivery_date,
    delivery_days = EXCLUDED.delivery_days,
    estimated_delivery_days = EXCLUDED.estimated_delivery_days,
    delivery_delay_days = EXCLUDED.delivery_delay_days,
    is_delivered = EXCLUDED.is_delivered,
    is_late_delivery = EXCLUDED.is_late_delivery;