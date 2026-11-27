
CREATE TABLE IF NOT EXISTS warehouse.fact_order_payments (
    payment_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    order_id VARCHAR(32) NOT NULL,
    payment_sequential INTEGER NOT NULL,

    customer_key BIGINT NOT NULL,

    payment_type VARCHAR(30),
    payment_installments INTEGER,
    payment_value NUMERIC(12,2) NOT NULL,

    CONSTRAINT uq_fact_payment
        UNIQUE (order_id, payment_sequential),

    CONSTRAINT fk_payment_customer
        FOREIGN KEY (customer_key)
        REFERENCES warehouse.dim_customer(customer_key)
);