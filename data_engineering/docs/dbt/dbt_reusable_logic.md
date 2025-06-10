
# 🛠️ Reusable Logic in DBT: Macros, Jinja Templates, and Redefined Transformations

## 📦 What is DBT?
DBT (Data Build Tool) is a modern data transformation framework that enables data analysts and engineers to transform data in their warehouse more effectively.

---

## 1. 📄 Macros

### ✅ What Are They?
Macros are reusable SQL snippets written using Jinja, which help avoid repeating logic.

### 🧪 Example: Date Truncation Macro
```sql
-- macros/date_trunc.sql
{% macro date_trunc(column, granularity='day') %}
    date_trunc('{{ granularity }}', {{ column }})
{% endmacro %}
```

### 💡 Usage in a Model
```sql
-- models/sensor_readings.sql
SELECT
    sensor_id,
    {{ date_trunc('reading_timestamp', 'hour') }} AS hourly_timestamp,
    reading_value
FROM {{ ref('raw_sensor_data') }}
```

---

## 2. 🧩 Jinja Templates

### ✅ What Is Jinja?
Jinja is a templating engine that powers DBT's dynamic SQL generation.

### 🧪 Example: Conditional Logic with Jinja
```sql
-- models/conditional_logic.sql
SELECT *
FROM {{ ref('sensor_data') }}
WHERE 1=1
{% if is_incremental() %}
  AND updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}
```

This template runs differently for full vs. incremental loads.

---

## 3. 🔁 Redefined Transformations

### ✅ Why Redefine?
To make your transformation logic modular and reusable across multiple models.

### 🧪 Example: Creating a Staging Model
```sql
-- models/staging/stg_sensor_data.sql
SELECT
    id,
    sensor_type,
    {{ date_trunc('timestamp', 'day') }} AS report_day
FROM {{ ref('raw_sensor_data') }}
```

Now use `stg_sensor_data` in multiple downstream models without duplicating logic.

---

## 💡 Best Practices

- Store macros in `macros/` directory.
- Use Jinja conditionals for dynamic logic.
- Reference other models using `{{ ref('model_name') }}` for maintainability.

---

## ✅ Conclusion

By using macros, Jinja templates, and modular SQL, you can write DRY, maintainable, and scalable transformation code in DBT.
