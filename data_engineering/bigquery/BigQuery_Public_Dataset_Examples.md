
# Expert BigQuery Interview Questions & Answers (with Public Datasets)

## 1. Advanced SQL & Analytics

**Q1. How does BigQuery handle window functions and how would you use them for calculating rolling averages or rankings?**  
A: BigQuery supports window functions like `RANK()`, `ROW_NUMBER()`, and `AVG()` over partitions.

📌 *Example: Rolling average of daily precipitation in LA*
```sql
SELECT
  date,
  value AS precipitation,
  AVG(value) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_avg
FROM `bigquery-public-data.ghcn_d.ghcnd_2020`
WHERE id = 'USC00115950'  -- Specific station
  AND element = 'PRCP'
  AND value IS NOT NULL
ORDER BY date
LIMIT 100;
```

**Q2. How would you use STRUCTs and ARRAYS in BigQuery? Give a use-case.**  
A: STRUCTs and ARRAYS allow nested and repeated fields.

📌 *Example: Create ARRAY of names per state from baby names*
```sql
SELECT state, ARRAY_AGG(STRUCT(name, number)) AS names
FROM `bigquery-public-data.usa_names.usa_1910_2013`
WHERE year = 2010
GROUP BY state
LIMIT 5;
```

**Q3. How do you handle nested and repeated fields in BigQuery?**  
📌 *Example: UNNEST GitHub repo topics*
```sql
SELECT repo.name, topic
FROM `bigquery-public-data.github_repos.repo_topics`, UNNEST(topic) AS topic
LIMIT 10;
```

**Q4. Month-over-month growth using window functions**  
📌 *Example: Monthly COVID-19 cases in US*
```sql
WITH monthly_cases AS (
  SELECT DATE_TRUNC(date, MONTH) AS month, SUM(cases) AS total_cases
  FROM `bigquery-public-data.covid19_jhu_csse.summary`
  WHERE country_region = 'US'
  GROUP BY month
)
SELECT month, total_cases,
       total_cases - LAG(total_cases) OVER (ORDER BY month) AS mom_growth
FROM monthly_cases;
```

**Q5. LEFT JOIN UNNEST vs CROSS JOIN UNNEST**  
📌 *Example: Demonstrate difference with GitHub repo licenses*
```sql
-- LEFT JOIN UNNEST (preserves rows with empty arrays)
SELECT r.name, l.license
FROM `bigquery-public-data.github_repos.repos` r
LEFT JOIN UNNEST([r.license]) AS l
LIMIT 5;
```

---

## 2. Performance Optimization & Cost Control

**Q1. Columnar Storage**  
BigQuery stores data in columnar format; querying only selected columns improves I/O and speed.

**Q2. Partitioning and Clustering**  
📌 *Example: Create a partitioned and clustered table from natality data*
```sql
CREATE OR REPLACE TABLE my_dataset.partitioned_births
PARTITION BY year
CLUSTER BY state AS
SELECT * FROM `bigquery-public-data.samples.natality`;
```

**Q3. Reduce Query Cost Strategies**  
- Use preview (`LIMIT`, column projection)
- Use date filters on partitioned tables
- Use materialized views and caching
- Cluster high-cardinality columns

**Q4. Materialized View**  
📌 *Example: Create materialized view on NYC taxi trip count*
```sql
CREATE MATERIALIZED VIEW my_dataset.mv_trips_per_day AS
SELECT DATE(pickup_datetime) AS trip_date, COUNT(*) AS trip_count
FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2018`
GROUP BY trip_date;
```

**Q5. Query Slots**  
Slots are virtual CPUs assigned for query stages. More slots = faster processing.

---

## 3. Architecture & Internals

Answers remain the same (conceptual).

---

## 4. Data Modeling & Pipeline Design

**Q1. Schema Design Best Practices**  
Use flat, denormalized structures. Use nested fields for arrays. Partition on time.

**Q2. Streaming IoT Data**  
Use Pub/Sub → Dataflow → BigQuery

**Q3. Denormalization**  
Improves read performance, useful in analytics.

**Q4. ELT over ETL**  
Do transformations in BigQuery after loading raw data.

**Q5. Schema Evolution**  
Use BigQuery's schema update options (`ALLOW_FIELD_ADDITION`).

**Q6. Load Large Files**  
📌 *Example: Load Parquet into BigQuery*
```bash
bq load --source_format=PARQUET my_dataset.my_table gs://my-bucket/data.parquet
```

---

## 5. Security, Access Control & Governance

**Q1. Row-level Security**  
📌 *Example: Create row access policy on state column*
```sql
CREATE ROW ACCESS POLICY state_filter
ON `project.dataset.births`
GRANT TO ("user@example.com")
FILTER USING (state = 'CA');
```

**Q2. Authorized View**  
Create a view and grant access to that view only.

**Q3. IAM Roles**  
Grant roles like `roles/bigquery.dataViewer` to restrict actions.

**Q4. Audit Logs**  
Use Cloud Logging → BigQuery Audit Logs.

**Q5. Role Difference**  
- `DATA_VIEWER`: read-only access  
- `BIGQUERY.USER`: query access but no data view unless granted

---

## 6. Integration with GCP & Tools

**Q1. Cloud Composer (Airflow)**  
Use `BigQueryInsertJobOperator` to run SQL from DAG.

**Q2. Export to GCS**  
📌 *Example: Export COVID-19 summary data*
```sql
EXPORT DATA OPTIONS (
  uri='gs://my-bucket/covid_summary.csv',
  format='CSV',
  overwrite=true
)
AS SELECT * FROM `bigquery-public-data.covid19_jhu_csse.summary`;
```

**Q3. Streaming**  
Use `bq insert`, Dataflow, or 3rd party tools.

**Q4. Dashboards**  
Use Looker Studio, Tableau, Power BI.

**Q5. BigQuery ML**  
Train ML models using SQL.

---

## 7. BigQuery ML & AI

**Q1. Limitations**  
No deep learning, limited algorithms.

**Q2. Use-case**  
📌 *Example: Predict baby name popularity*
```sql
CREATE OR REPLACE MODEL my_dataset.name_model
OPTIONS(model_type='linear_reg') AS
SELECT year, number FROM `bigquery-public-data.usa_names.usa_1910_2013`
WHERE name = 'Emma';
```

**Q3. Evaluate model**
```sql
SELECT * FROM ML.EVALUATE(MODEL `my_dataset.name_model`, (
  SELECT year, number FROM `bigquery-public-data.usa_names.usa_1910_2013`
  WHERE name = 'Emma'
));
```

**Q4. TensorFlow with BigQuery**  
Export data to GCS and train in Vertex AI or Colab.

---

## Case Study Prompts

**1. Optimization Prompt**  
📌 *Top 3 baby names by state in 2020*
```sql
SELECT state, name, total, rank FROM (
  SELECT state, name, SUM(number) AS total,
         RANK() OVER (PARTITION BY state ORDER BY SUM(number) DESC) AS rank
  FROM `bigquery-public-data.usa_names.usa_1910_2013`
  WHERE year = 2020
  GROUP BY state, name
)
WHERE rank <= 3;
```

**2. Streaming Design**  
Use IoT Core → Pub/Sub → Dataflow → BigQuery.

**3. Security Prompt**  
Create authorized views to restrict sensitive columns in public health datasets.
