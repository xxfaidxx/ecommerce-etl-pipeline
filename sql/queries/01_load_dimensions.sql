INSERT INTO warehouse.dim_customer (
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
)
SELECT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
FROM staging.stg_customers
ON CONFLICT (customer_id)
DO UPDATE SET
    customer_unique_id = EXCLUDED.customer_unique_id,
    customer_zip_code_prefix = EXCLUDED.customer_zip_code_prefix,
    customer_city = EXCLUDED.customer_city,
    customer_state = EXCLUDED.customer_state;


INSERT INTO warehouse.dim_product (
    product_id,
    product_category_name,
    product_category_name_english,
    product_name_length,
    product_description_length,
    product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
)
SELECT
    p.product_id,
    p.product_category_name,
    ct.product_category_name_english,
    p.product_name_lenght,
    p.product_description_lenght,
    p.product_photos_qty,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm
FROM staging.stg_products p
LEFT JOIN staging.stg_category_translation ct
    ON p.product_category_name = ct.product_category_name
ON CONFLICT (product_id)
DO UPDATE SET
    product_category_name = EXCLUDED.product_category_name,
    product_category_name_english = EXCLUDED.product_category_name_english,
    product_name_length = EXCLUDED.product_name_length,
    product_description_length = EXCLUDED.product_description_length,
    product_photos_qty = EXCLUDED.product_photos_qty,
    product_weight_g = EXCLUDED.product_weight_g,
    product_length_cm = EXCLUDED.product_length_cm,
    product_height_cm = EXCLUDED.product_height_cm,
    product_width_cm = EXCLUDED.product_width_cm;


INSERT INTO warehouse.dim_seller (
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
)
SELECT
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
FROM staging.stg_sellers
ON CONFLICT (seller_id)
DO UPDATE SET
    seller_zip_code_prefix = EXCLUDED.seller_zip_code_prefix,
    seller_city = EXCLUDED.seller_city,
    seller_state = EXCLUDED.seller_state;


INSERT INTO warehouse.dim_date (
    date_key,
    full_date,
    day,
    day_name,
    day_of_week,
    week_of_year,
    month,
    month_name,
    quarter,
    year,
    is_weekend
)
SELECT
    TO_CHAR(date_value, 'YYYYMMDD')::INTEGER,
    date_value::DATE,
    EXTRACT(DAY FROM date_value)::INTEGER,
    TO_CHAR(date_value, 'FMDay'),
    EXTRACT(ISODOW FROM date_value)::INTEGER,
    EXTRACT(WEEK FROM date_value)::INTEGER,
    EXTRACT(MONTH FROM date_value)::INTEGER,
    TO_CHAR(date_value, 'FMMonth'),
    EXTRACT(QUARTER FROM date_value)::INTEGER,
    EXTRACT(YEAR FROM date_value)::INTEGER,
    EXTRACT(ISODOW FROM date_value) IN (6, 7)
FROM GENERATE_SERIES(
    DATE '2016-01-01',
    DATE '2018-12-31',
    INTERVAL '1 day'
) AS date_value
ON CONFLICT (date_key)
DO NOTHING;
