# Advanced SQL & Analytics with BigQuery

## 1. Window Functions in BigQuery

### Background & Reasoning

Window functions allow computations across rows without aggregating results, ideal for rolling averages or rankings.

### BigQuery Internals

- **Columnar storage** improves IO efficiency.
- **Parallel execution** across slots ensures rapid results.

### Pros and Cons

- **Pros:** High-speed analytics, maintains granularity.
- **Cons:** Can incur costs if sorting large partitions.

### Example Query (Rolling Average):

```sql
SELECT
  date,
  product_category,
  sales,
  AVG(sales) OVER (
    PARTITION BY product_category
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS rolling_7_day_avg
FROM (
  SELECT
    DATE(order_date) AS date,
    product_category,
    SUM(sale_price) AS sales
  FROM
    `bigquery-public-data.thelook_ecommerce.orders`
  GROUP BY
    date, product_category
)
ORDER BY product_category, date;
```

### Practical Task

- Write a query to identify the top 3 products per category by monthly sales from `thelook_ecommerce`.

## 2. STRUCTs and ARRAYS

### Usage

- STRUCTs hold nested records.
- ARRAYS handle repeated fields.

### Use Case

- Order details with multiple products stored in nested arrays.

## 3. Nested and Repeated Fields

### Performance Impact

- Improved JOIN performance by minimizing external joins.

### Pros and Cons

- **Pros:** Faster reads, reduced complexity.
- **Cons:** Complex schema, harder to manage schema evolution.

## 4. Month-over-Month Growth

### Example Query:

```sql
WITH monthly_sales AS (
  SELECT
    FORMAT_DATE('%Y-%m', DATE(order_date)) AS month,
    SUM(sale_price) AS total_sales
  FROM
    `bigquery-public-data.thelook_ecommerce.orders`
  GROUP BY month
)
SELECT
  month,
  total_sales,
  LAG(total_sales) OVER (ORDER BY month) AS prev_month_sales,
  ROUND(((total_sales - LAG(total_sales) OVER (ORDER BY month)) / LAG(total_sales) OVER (ORDER BY month)) * 100, 2) AS mom_growth
FROM monthly_sales;
```

## 5. JOIN EACH vs Regular Joins

- `JOIN EACH` (deprecated) forced distributed joins.
- Regular joins auto-optimize.

## 6. LEFT JOIN UNNEST() vs Cross Join UNNEST()

- LEFT JOIN retains all left-side rows; CROSS JOIN expands arrays fully.

# Performance Optimization & Cost Control

## 1. Columnar Storage

- Reduces IO by reading relevant columns only.

## 2. Partitioning & Clustering

- **Partitioning:** Optimizes queries by date ranges.
- **Clustering:** Optimizes queries by sorting data within partitions.

## 3. Cost Reduction Strategies

1. Partitioning and clustering.
2. Columnar selectivity.
3. Materialized views.
4. Efficient schema design.
5. Query pruning.

## 4. Materialized vs Regular Views

- Materialized views physically store data, enhancing performance.

## 5. Query Slots

- Compute units allocated dynamically based on pricing models.

## 6. Query Optimization

- Limit scans via filtering, partitions, clustering.

# Architecture & Internals

## BigQuery Architecture

- **Dremel:** Query engine.
- **Colossus:** Distributed columnar storage.

## Storage & Compute Separation

- Enables scalability and flexible cost management.

## Query Execution Stages

1. Parsing
2. Planning
3. Execution
4. Aggregation

## Slots & Pricing

- Dynamic: Pay-per-use.
- Flat-rate: Fixed cost, reserved resources.

## Data Consistency

- Replicated and managed via distributed Colossus storage.

# Data Modeling & Pipeline Design

## Schema Design

- Favor denormalization and nested structures.

## IoT Data Pipeline

- Use Pub/Sub → Dataflow → BigQuery streaming inserts.

## Denormalization

- Simplifies queries, but increases storage.

## ELT vs ETL

- ELT is preferred in BigQuery for flexibility and performance.

## Schema Evolution

- Use safe schema updates (adding columns) to avoid disruption.

## Efficient File Loading

- Use Avro/Parquet for fast and efficient bulk loads.

# Security, Access Control & Governance

## Row-level Security

- Implement via policy tags and row access policies.

## Authorized Views

- Limit data access through controlled views.

## IAM Roles

- Use granular permissions (`bigquery.dataViewer` vs `bigquery.user`).

## Auditing

- Use BigQuery audit logs.

# Integration with GCP & Tools

## Workflow Orchestration

- Cloud Composer (Airflow) integrates seamlessly.

## Export to GCS

- Schedule exports via Cloud Composer or Scheduled Queries.

## Streaming Options

- Pub/Sub, Dataflow, direct streaming inserts.

## Dashboards

- Connect to Looker Studio, Tableau via direct connectors.

## BigQuery ML

- Train and deploy models directly within BigQuery.

# BigQuery ML & AI Integration

## Limitations

- Suitable for common models; limited deep learning capabilities.

## Use Case

- Customer churn prediction using logistic regression within BigQuery ML.

## Model Evaluation

- Monitor via built-in ML metrics (ROC, accuracy).

## TensorFlow Integration

- BigQuery ML supports importing external TensorFlow models for advanced scenarios.

