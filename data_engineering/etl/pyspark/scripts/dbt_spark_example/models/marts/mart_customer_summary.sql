SELECT
    customer_id,
    COUNT(*) AS total_orders
FROM {{ ref('stg_customers') }}
JOIN {{ source('raw', 'orders') }} USING (customer_id)
GROUP BY customer_id