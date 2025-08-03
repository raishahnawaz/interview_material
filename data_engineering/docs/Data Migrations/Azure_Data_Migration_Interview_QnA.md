
# Azure Data Migration Interview Questions and Sample Answers

## 🔹 Migration Strategy & Architecture

### 1. Can you walk us through your end-to-end strategy for migrating on-premise SQL Server or MySQL data to Azure Synapse or Azure Data Lake?
**Answer:** 
Begin with assessment of source systems to understand schema, volume, and dependencies. Use Azure Data Migration Assistant (DMA) for compatibility checks. Plan a phased migration starting with schema deployment to target (Synapse/ADLS). Use Azure Database Migration Service (DMS) or custom ADF pipelines for data transfer. Implement data validation and reconciliation. Apply incremental loads using watermarking or Change Data Capture (CDC) until full cutover.

### 2. What factors do you consider when deciding between Azure Synapse and Azure Data Lake for storing migrated data?
**Answer:** 
Choose Synapse for structured, relational analytics and SQL-based transformations. Prefer ADLS for storing raw/semi-structured data or when using big data processing tools like Databricks. Consider factors like query latency, user access patterns, transformation complexity, and cost.

### 3. How would you handle a scenario where legacy systems are still actively being used during the migration (i.e., live incremental changes)?
**Answer:** 
Use hybrid migration. Perform full load initially, then set up incremental sync using CDC, timestamps, or triggers. Schedule periodic ADF jobs or use tools like Azure DMS to maintain parity. Plan final switchover during a low-activity window.

### 4. What’s your approach to migrating SSRS-based reporting systems to cloud-native reporting in Azure?
**Answer:** 
First analyze existing reports and datasets. Recreate core datasets in Azure SQL or Synapse. Rebuild reports in Power BI or migrate to paginated reports in Power BI Premium. Use shared datasets for reusability and RBAC for access control.

### 5. Have you used the Azure Database Migration Service (DMS)? If so, how do you integrate it into your broader pipeline?
**Answer:** 
Yes, DMS is used for schema and data migration. It can be triggered separately or orchestrated from ADF using webhook or Azure Functions. Its logs can be monitored to validate completion before downstream ETL begins.

## 🔹 ETL / Data Pipeline Design

### 6. How do you structure ADF pipelines to be modular, reusable, and environment-agnostic?
**Answer:** 
Use parameterized pipelines and datasets. Externalize environment-specific settings in configuration tables or key vaults. Break down logic into child pipelines using `Execute Pipeline` activity. Maintain DRY principles using custom templates.

### 7. How do you manage dependencies and control flow across multiple pipelines and activities in ADF?
**Answer:** 
Use dependencies via success/failure outputs of activities. For complex flows, leverage pipeline chaining and tumbling window triggers. Use lookup activities to fetch control metadata and `If Condition`/`Switch` for branching.

### 8. When would you prefer Azure Data Factory over Azure Databricks or Synapse Pipelines?
**Answer:** 
ADF is ideal for orchestration and simple transformations. Databricks suits complex data wrangling, ML, and PySpark workflows. Synapse Pipelines offer tighter integration for SQL-based processing. Choose based on team skills, complexity, and performance needs.

### 9. Can you share your experience implementing slowly changing dimensions (SCD Type 1/2) using ADF or SQL?
**Answer:** 
Use data flow in ADF for comparing incoming vs existing data. Use `Surrogate Key` and `Alter Row` transformations to handle insert/update logic. For Type 2, manage `start_date`, `end_date`, and `is_current` fields accordingly.

### 10. What is your approach to parameterizing pipelines in ADF for dynamic loading from multiple sources?
**Answer:** 
Create metadata-driven control tables with source/target mappings. Use `Lookup` and `ForEach` to iterate over configurations. Parameters are injected at runtime to datasets, linked services, and activities for flexibility.

## 🔹 Data Validation, Logging & Monitoring

### 11. What mechanisms do you use for data validation post-migration?
**Answer:** 
Row counts, checksums, and sample value comparisons. Use validation scripts in SQL or Python. Automate post-load QA using ADF data flows or integration with testing frameworks.

### 12. How do you implement logging and error handling in ADF pipelines?
**Answer:** 
Use custom logging with `Stored Procedure` or `Web Activity` to write logs. Use `On Failure` activities to handle errors. Collect metrics into Azure Log Analytics for centralized monitoring.

### 13. Have you integrated Azure Monitor or Log Analytics with ADF pipelines? If so, how do you use those insights?
**Answer:** 
Yes. Monitor pipeline runs, trigger failures, and performance metrics. Setup alerts on anomalies like prolonged runtimes or high failure rates. Use dashboards to visualize SLA adherence and system health.

## 🔹 Performance Optimization & Tuning

### 14. What common performance issues have you faced in Azure Data Factory or Synapse, and how did you resolve them?
**Answer:** 
Bottlenecks often arise from source limits, data skew, or large shuffles in transformations. Solutions include partitioning, filtering early, using staging tables, and tuning DWU settings in Synapse.

### 15. How do you approach performance tuning in a large-scale data migration involving complex transformations?
**Answer:** 
Benchmark each step. Use ADF Data Flows with optimized sinks. Push filters upstream. Split large data loads into smaller partitions. Use PolyBase or COPY for efficient Synapse ingestion.

### 16. Have you implemented partitioning strategies for better performance in Synapse or Data Lake?
**Answer:** 
Yes. For Synapse, use `HASH` or `ROUND_ROBIN` distributions based on join keys. For ADLS, partition folders by date or region. This improves pruning and parallelism.

## 🔹 Data Modeling & Warehouse Design

### 17. How do you handle schema mapping and transformations during the migration process?
**Answer:** 
Create a mapping document upfront. Use ADF Data Flow or mapping dataflows. Apply transformations inline or in SQL staging scripts. Automate schema validations using schema comparison tools.

### 18. Can you describe your experience with dimensional modeling (star/snowflake)?
**Answer:** 
Yes. Design facts for measurable events, and dimensions for descriptive attributes. Star schemas for simplicity and performance. Snowflake when normalization is required. Ensure surrogate keys, audit columns, and indexing.

### 19. What’s your preferred approach for managing metadata-driven ETL pipelines?
**Answer:** 
Maintain metadata tables for source-target mappings, transformations, file paths, schedule frequency. Use these tables to dynamically build pipeline logic using ADF’s `Lookup`, `ForEach`, and parameterization features.

## 🔹 CI/CD & Agile Delivery

### 20. What’s your experience with CI/CD for ADF pipelines using Azure DevOps or GitHub Actions?
**Answer:** 
Use Git integration in ADF. Develop in feature branches, use pull requests. Use YAML pipelines in DevOps to automate ARM template deployment. Parameterize templates for multi-env deploys.

### 21. How do you manage version control and deployment of data pipelines across multiple environments?
**Answer:** 
Use Git branches for environments. Maintain environment-specific ARM templates or Key Vault references. Automate deployments using CI/CD with proper rollback and approvals.

### 22. Have you worked in Agile environments? How do you align data migration tasks with sprint goals?
**Answer:** 
Yes. Break down migration into epics like ingestion, transformation, validation. Each sprint targets a set of tables or pipelines. Use JIRA or Azure Boards for task tracking. Perform daily stand-ups and reviews.

## 🔹 Governance, Security & Cost

### 23. How do you ensure data governance and security during cloud migration?
**Answer:** 
Use Azure RBAC, data masking, and encryption (at rest and in transit). Monitor access using Azure Defender. Classify and tag sensitive data. Maintain audit trails and logging.

### 24. What’s your approach to cost monitoring and optimization in Azure data services?
**Answer:** 
Use Azure Cost Management. Prefer serverless and on-demand services where applicable. Monitor DWUs in Synapse. Avoid unnecessary data movement and idle resources.

### 25. How do you manage data lineage and documentation in a large-scale migration project?
**Answer:** 
Use tools like Azure Purview or create custom lineage using pipeline metadata. Document mappings, logic, and dependencies. Maintain versioned documentation in Confluence or Git repositories.
