CREATE TABLE IF NOT EXISTS warehouse.fact_orders (
    order_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    order_id VARCHAR(32) NOT NULL UNIQUE,
    customer_key BIGINT NOT NULL,

    order_date_key INTEGER,
    approved_date_key INTEGER,
    delivered_carrier_date_key INTEGER,
    delivered_customer_date_key INTEGER,
    estimated_delivery_date_key INTEGER,

    order_status VARCHAR(30) NOT NULL,

    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,

    delivery_days INTEGER,
    estimated_delivery_days INTEGER,
    delivery_delay_days INTEGER,

    is_delivered BOOLEAN NOT NULL DEFAULT FALSE,
    is_late_delivery BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_fact_orders_customer
        FOREIGN KEY (customer_key)
        REFERENCES warehouse.dim_customer(customer_key),

    CONSTRAINT fk_fact_orders_purchase_date
        FOREIGN KEY (order_date_key)
        REFERENCES warehouse.dim_date(date_key),

    CONSTRAINT fk_fact_orders_approved_date
        FOREIGN KEY (approved_date_key)
        REFERENCES warehouse.dim_date(date_key),

    CONSTRAINT fk_fact_orders_carrier_date
        FOREIGN KEY (delivered_carrier_date_key)
        REFERENCES warehouse.dim_date(date_key),

    CONSTRAINT fk_fact_orders_customer_delivery_date
        FOREIGN KEY (delivered_customer_date_key)
        REFERENCES warehouse.dim_date(date_key),

    CONSTRAINT fk_fact_orders_estimated_date
        FOREIGN KEY (estimated_delivery_date_key)
        REFERENCES warehouse.dim_date(date_key)
);