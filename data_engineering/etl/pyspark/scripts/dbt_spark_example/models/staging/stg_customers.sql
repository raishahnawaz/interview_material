SELECT
    id AS customer_id,
    first_name,
    last_name,
    created_at
FROM {{ source('raw', 'customers') }}