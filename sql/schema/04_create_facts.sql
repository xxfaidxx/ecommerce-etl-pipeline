
CREATE TABLE IF NOT EXISTS warehouse.fact_order_items (
    order_item_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    order_id VARCHAR(32) NOT NULL,
    order_item_id INTEGER NOT NULL,

    customer_key BIGINT NOT NULL,
    product_key BIGINT NOT NULL,
    seller_key BIGINT NOT NULL,
    order_date_key INTEGER NOT NULL,

    shipping_limit_date TIMESTAMP,
    price NUMERIC(12,2) NOT NULL,
    freight_value NUMERIC(12,2) NOT NULL,

    CONSTRAINT uq_fact_order_item
        UNIQUE (order_id, order_item_id),

    CONSTRAINT fk_fact_customer
        FOREIGN KEY (customer_key)
        REFERENCES warehouse.dim_customer(customer_key),

    CONSTRAINT fk_fact_product
        FOREIGN KEY (product_key)
        REFERENCES warehouse.dim_product(product_key),

    CONSTRAINT fk_fact_seller
        FOREIGN KEY (seller_key)
        REFERENCES warehouse.dim_seller(seller_key),

    CONSTRAINT fk_fact_order_date
        FOREIGN KEY (order_date_key)
        REFERENCES warehouse.dim_date(date_key)
);
