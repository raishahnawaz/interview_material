# 📘 Descriptive Guide to Understanding Apache Tez

Apache Tez is a powerful and flexible framework designed to build data processing applications that run on top of Hadoop YARN. It represents a significant leap from the traditional MapReduce model by enabling a more efficient execution of complex DAGs (Directed Acyclic Graphs) for data computation.

---

## 🔹 What is Apache Tez?
Apache Tez is an application framework which allows for a complex Directed Acyclic Graph of tasks for processing data. It is used primarily to optimize the performance of frameworks like Apache Hive and Apache Pig.

### ✨ Key Highlights:
- **Optimized DAG execution** instead of rigid MapReduce phases.
- **Interactive & Batch support**.
- **YARN-native**: Fully integrated into the Hadoop ecosystem.
- **Highly tunable**: Resource allocation, DAG fusion, parallelism.

---

## 🔧 Apache Tez Architecture

### 🧩 Core Components:
1. **DAG (Directed Acyclic Graph)** – Represents your computation as a series of vertices (tasks) and edges (data flow).
2. **Tez Application Master (AM)** – Manages DAG execution.
3. **Tez Task** – Unit of execution (vertex instance).
4. **Input/Output/Processor** – Custom interfaces to control the flow of data and logic.

### ♲ Execution Lifecycle:
1. Client submits DAG.
2. AM is launched on YARN.
3. Vertices scheduled dynamically based on execution.
4. Intermediate results passed across vertices.
5. Final output committed.

---

## 🚀 Advantages of Tez over MapReduce
| Feature | MapReduce | Apache Tez |
|--------|------------|------------|
| Processing Model | Fixed phases (Map -> Shuffle -> Reduce) | Arbitrary DAG |
| Performance | High latency | Low latency (suitable for interactive queries) |
| Resource Usage | Less efficient | Dynamic and optimized |
| Reuse | No | Container reuse, pipelining |

---

## 📌 Use Cases
- **Apache Hive on Tez**: Speeds up SQL-like querying by reducing unnecessary data scans and improving job coordination.
- **Pig on Tez**: Similar benefits for script-based ETL workflows.
- **Custom DAG-based apps**: You can define your own data processing logic.

---

## 📌 Example Code: Custom DAG using Apache Tez

This Java-based code sets up a simple Tez job, with 2 vertices:
(See `SimpleTezDAG.java`)

---

## ⚙️ Running Apache Tez on Kubernetes (K8s)

### Dockerfile (Tez Base Image)
(See `Dockerfile`)

### K8s Deployment (simplified for Minikube or KinD)
(See `tez-pod.yaml`)

---

## 🧠 Apache Tez Interview Questions

### Basic:
**Q1: What is Apache Tez and how does it differ from MapReduce?**  
Apache Tez is an advanced data processing framework that builds complex DAGs of tasks, allowing for more fine-grained control and efficiency compared to MapReduce's rigid Map -> Reduce phases. Unlike MapReduce, Tez supports container reuse, reduces I/O operations, and minimizes latency by enabling pipelined execution.

**Q2: Explain DAG execution in Tez.**  
In Tez, a DAG represents a job as vertices (logical units of work) and edges (data movement). Each vertex is executed once its dependencies are met, and data is passed through edges using input/output descriptors. The DAG is submitted to the Tez Application Master which orchestrates execution.

**Q3: What are the advantages of using Tez over traditional Hadoop?**  
- Lower latency and higher throughput
- Container reuse reduces overhead
- Better resource utilization via YARN
- Fine-grained optimization of data flows
- Native support for DAG-based execution logic

### Intermediate:
**Q4: How does Tez improve the performance of Hive?**  
Hive translates SQL queries into Tez DAGs, allowing for fewer intermediate steps, reduced data shuffling, and more optimized resource usage. This results in faster query execution and better scalability.

**Q5: What is the role of the Application Master in Tez?**  
The Tez Application Master (AM) coordinates the execution of DAGs, manages task scheduling, resource allocation via YARN, monitors task progress, and handles task retries or failures.

**Q6: How can you tune resource allocation in a Tez job?**  
By configuring parameters such as:
- `tez.task.resource.memory.mb`
- `tez.task.resource.cpu.vcores`
- `tez.am.resource.memory.mb`
- DAG parallelism and split sizes
These help optimize task execution time and memory footprint.

### Advanced:
**Q7: Describe how container reuse works in Tez.**  
Tez supports container reuse to reduce the overhead of launching new containers for each task. A single container can be used to execute multiple tasks sequentially, improving efficiency and reducing YARN scheduling delays.

**Q8: Explain how fault tolerance is managed in Tez.**  
Tez retries failed tasks based on configurable policies, reuses lineage metadata to recompute failed tasks efficiently, and can recover from node failures by reassigning tasks to healthy containers. Tez also supports DAG recovery across AM restarts.

**Q9: How would you debug a failed Tez DAG execution?**  
- Check Tez UI and YARN ResourceManager logs
- Analyze logs from the failed container
- Use counters and metrics from DAGClient
- Enable verbose logging for input/output/processor classes
- Validate resource allocation and environment settings

---

## 📚 Case Studies

### 📌 Case Study 1: Hive Query Optimization
- A large retail company migrated from Hive-on-MapReduce to Hive-on-Tez.
- Result: Query latency dropped by 60%, daily ETL jobs finished 3 hours earlier.

### 📌 Case Study 2: Custom DAGs for Machine Learning Pipeline
- A data science team used Tez DAGs to build a pipeline for large-scale feature extraction.
- Result: Reduced I/O bottlenecks, efficient use of intermediate data, faster iteration.

---

## ✅ Conclusion
Apache Tez provides a scalable, efficient, and flexible execution model for big data applications. Whether you're improving query performance on Hive or building your own DAG-based processing, Tez offers architectural and performance benefits worth considering — especially in modern Hadoop or Kubernetes-native environments.
