
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

### 🔄 Execution Lifecycle:
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

## 📎 Example Code: Custom DAG using Apache Tez

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
1. What is Apache Tez and how does it differ from MapReduce?
2. Explain DAG execution in Tez.
3. What are the advantages of using Tez over traditional Hadoop?

### Intermediate:
4. How does Tez improve the performance of Hive?
5. What is the role of the Application Master in Tez?
6. How can you tune resource allocation in a Tez job?

### Advanced:
7. Describe how container reuse works in Tez.
8. Explain how fault tolerance is managed in Tez.
9. How would you debug a failed Tez DAG execution?

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
