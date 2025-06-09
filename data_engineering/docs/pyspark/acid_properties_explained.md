
# 🧪 Understanding ACID Properties in Databases

ACID is an acronym that represents the four key properties that ensure reliable processing of database transactions.

| Property  | Description |
|-----------|-------------|

## 🔹 A — Atomicity
**"All or nothing"**: A transaction is treated as a single unit.  
- Either **all operations** in a transaction are completed, or **none** are.
- If a failure occurs at any step, the database is rolled back to its previous state.

✅ Example:  
Transferring money from Account A to B — if debit succeeds but credit fails, the transaction should be rolled back.

---

## 🔹 C — Consistency
**"Valid state transition"**: A transaction must bring the database from one valid state to another.

- Enforces **integrity constraints** (like primary keys, foreign keys, or business rules).
- Prevents corrupt or invalid data from being written.

✅ Example:  
If a column must not accept NULLs, the database will reject transactions that violate this rule.

---

## 🔹 I — Isolation
**"Transactions don't interfere with each other"**: The intermediate state of a transaction is **invisible** to other concurrent transactions.

- Ensures **concurrent transactions** produce the same results as if they were executed sequentially.
- Managed by **isolation levels** (Read Committed, Repeatable Read, Serializable, etc.).

✅ Example:  
Two people booking the last seat on a flight simultaneously — only one should succeed.

---

## 🔹 D — Durability
**"Once committed, always committed"**: After a transaction is completed, the data changes are **permanent**, even in the case of a crash.

- Ensures that committed data is saved to **non-volatile storage**.
- Guarantees reliability after power loss or system failure.

✅ Example:  
If a purchase order is confirmed, it should remain in the database even after a server reboot.

---

## 🔍 Summary Table

| Property   | Ensures That...                              |
|------------|----------------------------------------------|
| Atomicity  | Transactions are fully completed or aborted  |
| Consistency| Only valid data is written to the database   |
| Isolation  | Transactions don’t impact each other         |
| Durability | Committed data is never lost                 |

---

## 🏁 Use Cases
- Financial systems (e.g., banking, trading platforms)
- Inventory/order management
- Systems where data integrity is critical

