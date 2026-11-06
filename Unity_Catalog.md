
## 1. When large amounts of data arrive, what happens?

When an organization works with large amounts of data, that data can come from different departments, applications, databases, and external systems.

For example:

- HR systems provide employee, salary, and attendance data.
- Finance systems provide payments, expenses, and budget data.
- Sales applications provide customer, order, and revenue data.
- Websites and applications generate logs and event data.
- Document systems provide PDFs, Excel files, images, and other documents.

The data does not always arrive in one format. It may arrive as files, database records, or data received through APIs.

## 2. In which formats can data arrive?

Some common formats are:

| Format / Source | What it contains | Example |
|---|---|---|
| CSV | Text arranged in rows and columns | `employees.csv` |
| Excel | Spreadsheet data | `employees.xlsx` |
| JSON | Structured key-value data, often received from APIs | `customers.json` |
| Parquet | Column-oriented data format used for analytics | `sales.parquet` |
| Avro | Data serialization format often used in data pipelines | `events.avro` |
| XML | Structured, tagged data | `orders.xml` |
| Database tables | Rows and columns stored in a database | SQL Server employee table |
| PDF / Word / Images | Documents and other files | `offer_letter.pdf` |

CSV, Excel, JSON, Parquet, Avro, and XML describe data/file formats. SQL Server, MySQL, and PostgreSQL are database systems. An API is a way for applications to exchange data.

## 3. Where is the actual data stored?

This is important to understand before learning Unity Catalog.

**Unity Catalog does not physically store all the organization's data.** The actual data files are stored in a storage system, such as:

- Amazon S3
- Azure Data Lake Storage (ADLS)
- Google Cloud Storage

Databricks reads, processes, and writes data in these storage locations.

For example, when an organization uploads `employees.csv`, the original file may be kept in cloud storage. Databricks can read that CSV, process it, and save the result as a Delta table.

### Physical storage and Unity Catalog are different

| Physical storage | Unity Catalog |
|---|---|
| Holds the actual data files. | Organizes and governs data assets. |
| Stores files such as Parquet data files and Delta transaction logs. | Maintains metadata such as names, schemas, ownership, permissions, and storage locations. |
| Examples: S3, ADLS, Google Cloud Storage. | Contains Metastores, Catalogs, Schemas, Tables, Views, and Volumes. |

Think of physical storage as the place where the actual data is kept. Unity Catalog is the organization and governance layer that helps Databricks understand, find, and control access to those data assets.

## 4. What happens to incoming data in Databricks?

A common data flow looks like this:

```text
Data sources
(CSV, Excel, JSON, databases, APIs, Parquet)
                  |
                  v
             Data ingestion
                  |
                  v
       Cloud storage / landing area
                  |
                  v
       Databricks reads the data
                  |
                  v
        Data processing using Spark
                  |
                  v
       Data written as Delta tables
                  |
                  v
       Unity Catalog organizes and governs
                  |
                  v
        Queries, reports and analytics
```

The incoming format does not have to be the same as the final table format.

For example:

```text
employees.csv
      |
      | Databricks reads the CSV
      v
Spark DataFrame
      |
      | Data is written in Delta format
      v
hr_catalog.employee.employees
```

The original CSV can remain in its original location. The Delta table is a separate table stored in cloud storage.

## 5. How does Unity Catalog organize data?

Unity Catalog follows this hierarchy:

```text
Metastore
    |
    v
Catalog
    |
    v
Schema
    |
    +----------+-----------+
    |          |           |
    v          v           v
  Table      View       Volume
```

Let's understand what each object does and, importantly, whether it physically stores data.

### 5.1 Metastore

A Metastore is the top-level container in Unity Catalog for organizing and governing data assets.

It maintains metadata about the catalogs and the assets registered under them.

It helps manage:

- Catalogs and their organization
- Data ownership
- Permissions and access control
- Data discovery and governance
- Information about managed and external storage locations

**Does the Metastore store actual data?**

No. The Metastore stores and manages metadata and governance information. The actual data files remain in cloud storage.

Example:

```text
abc_metastore
```

A Metastore is generally assigned to Databricks workspaces in a particular cloud region. It is created and managed by an account administrator. Many workspaces already have one assigned.

### 5.2 Catalog

A Catalog is a major grouping of data assets inside a Metastore.

An organization can create catalogs based on departments, business units, environments, or governance requirements.

For example:

```text
abc_metastore
    |
    +-- hr_catalog
    |
    +-- finance_catalog
    |
    +-- sales_catalog
    |
    +-- marketing_catalog
```

- `hr_catalog` groups HR-related data assets.
- `finance_catalog` groups finance-related data assets.
- `sales_catalog` groups sales-related data assets.

**Does a Catalog store actual data?**

No. A Catalog is a logical container. It organizes schemas and other Unity Catalog objects and maintains their metadata and governance information. It does not itself hold the actual employee or sales records.

### 5.3 Schema

A Schema is a container inside a Catalog. It groups related tables, views, and volumes.

For example:

```text
hr_catalog
    |
    +-- employee
    |
    +-- payroll
    |
    +-- attendance
    |
    +-- performance
```

- `employee` contains employee-related assets.
- `payroll` contains salary and payment-related assets.
- `attendance` contains attendance-related assets.
- `performance` contains performance-related assets.

**Does a Schema store actual data?**

No. A Schema is also a logical container. It organizes data objects and maintains their metadata. The actual table data or files are stored in the underlying storage system.

### 5.4 Tables

A Table is where we access structured data in rows and columns.

For example:

```text
hr_catalog.employee.employees
```

| emp_id | emp_name | department | salary |
|---:|---|---|---:|
| 101 | Rahul | IT | 50000 |
| 102 | Priya | HR | 45000 |
| 103 | Amit | Sales | 60000 |

When we create a managed Delta table, Databricks manages the table's underlying data files in cloud storage. Unity Catalog maintains the table's metadata and governs access to it.

So, unlike a Metastore, Catalog, or Schema, a table represents actual structured data stored in the underlying storage.

**What format is used for tables?**

Databricks commonly uses Delta Lake format for tables. Delta Lake stores data in Parquet files and maintains a transaction log to support reliable table operations.

Incoming CSV or JSON data can be read and written as a Delta table.

Example:

```text
Incoming CSV
     |
     v
Read and process
     |
     v
Delta table
```

### 5.5 Views

A View is a saved SQL query that presents data from one or more tables.

Suppose an employee table contains:

- Employee ID
- Employee name
- Department
- Salary

A manager may need only employee ID, name, and department. We can create a view that selects those columns.

```sql
CREATE VIEW hr_catalog.employee.employee_public_view AS
SELECT
    emp_id,
    emp_name,
    department
FROM hr_catalog.employee.employees;
```

Now we can query:

```sql
SELECT *
FROM hr_catalog.employee.employee_public_view;
```

**Does a normal View store actual data?**

No. A standard view stores the SQL query definition, not a separate copy of the table records. When the view is queried, Databricks runs the query against its underlying data.

A materialized view is different: it stores precomputed results. But a normal view does not.

### 5.6 Volumes

A Volume is a Unity Catalog object used to organize and govern files that are not necessarily tables.

Examples:

- PDF documents
- Excel files
- CSV files waiting to be processed
- Images
- JSON files
- Word documents

For example:

```text
hr_catalog.employee.hr_documents
```

This Volume can contain HR-related documents.

**Does a Volume store actual files?**

Yes. A Volume provides a governed location for files in underlying cloud storage. Unity Catalog manages the Volume's metadata and access permissions, while the actual file contents are stored in the underlying storage.

A CSV file inside a Volume does not automatically become a table. We must read and process it if we want to create a table from it.

## 6. One example of the complete Unity Catalog structure

Suppose an organization receives data from HR, Finance, and Sales.

It can organize the data like this:

```text
abc_metastore
|
+-- hr_catalog
|   |
|   +-- employee
|   |   |
|   |   +-- employees                 (Table)
|   |   +-- employee_public_view      (View)
|   |   +-- hr_documents              (Volume)
|   |
|   +-- payroll
|   |   |
|   |   +-- salary_details            (Table)
|   |
|   +-- attendance
|       |
|       +-- attendance_records        (Table)
|
+-- finance_catalog
|   |
|   +-- transactions
|   |   |
|   |   +-- payments                  (Table)
|   |
|   +-- budget
|       |
|       +-- department_budget         (Table)
|
+-- sales_catalog
    |
    +-- customers
    |   |
    |   +-- customer_details          (Table)
    |
    +-- orders
        |
        +-- orders                    (Table)
```

The full name of a table is:

```text
catalog.schema.table
```

For example:

```text
hr_catalog.employee.employees
```

Here:

- `hr_catalog` is the Catalog.
- `employee` is the Schema.
- `employees` is the Table.

This is called the three-level namespace.

## 7. How can we create these objects?

Once a Unity Catalog Metastore is assigned to the workspace and we have the required permissions, we can create catalogs and schemas using SQL.

### Create Catalogs

```sql
CREATE CATALOG IF NOT EXISTS hr_catalog;

CREATE CATALOG IF NOT EXISTS finance_catalog;

CREATE CATALOG IF NOT EXISTS sales_catalog;
```

### Create Schemas

```sql
CREATE SCHEMA IF NOT EXISTS hr_catalog.employee;

CREATE SCHEMA IF NOT EXISTS hr_catalog.payroll;

CREATE SCHEMA IF NOT EXISTS hr_catalog.attendance;
```

### Create a Volume

```sql
CREATE VOLUME IF NOT EXISTS
hr_catalog.employee.hr_documents;
```

### Create a Delta Table

```sql
CREATE TABLE hr_catalog.employee.employees
(
    emp_id INT,
    emp_name STRING,
    department STRING,
    salary DOUBLE
)
USING DELTA;
```

### Insert sample data

```sql
INSERT INTO hr_catalog.employee.employees
VALUES
(101, 'Rahul', 'IT', 50000),
(102, 'Priya', 'HR', 45000),
(103, 'Amit', 'Sales', 60000);
```

### Read the table

```sql
SELECT *
FROM hr_catalog.employee.employees;
```

### Create a View

```sql
CREATE VIEW hr_catalog.employee.employee_public_view AS
SELECT emp_id, emp_name, department
FROM hr_catalog.employee.employees;
```

### Check created objects

```sql
SHOW CATALOGS;

SHOW SCHEMAS IN hr_catalog;

SHOW TABLES IN hr_catalog.employee;

DESCRIBE TABLE hr_catalog.employee.employees;
```

These commands create the logical objects and table shown above. The Metastore itself is created and assigned through the Databricks account administration interface, not with the ordinary catalog/schema SQL commands.

## 8. Quick comparison: What stores data and what organizes data?

| Unity Catalog object | Main purpose | Does it hold actual data? |
|---|---|---|
| Metastore | Top-level metadata and governance | No |
| Catalog | Groups data assets | No |
| Schema | Groups related assets inside a Catalog | No |
| Table | Represents structured records | Yes, underlying table data is stored in cloud storage |
| Normal View | Presents data using a saved SQL query | No separate copy of the underlying data |
| Volume | Provides governed file storage | Yes, actual files are stored in underlying cloud storage |

Remember: Unity Catalog is the governance and organization layer. The actual contents of tables and files are held in the underlying storage.

## 9. Final concept to remember

When large organizational data arrives:

1. It can arrive as CSV, Excel, JSON, Parquet, database records, API data, PDFs, and other formats.
2. The data is received through ingestion processes and stored in cloud storage.
3. Databricks reads and processes the incoming data.
4. Structured data can be written as Delta tables.
5. Unity Catalog organizes and governs those assets using its hierarchy:
   - **Metastore:** top-level governance container.
   - **Catalog:** major grouping of data assets.
   - **Schema:** grouping of related tables, views, and volumes.
   - **Table:** structured, queryable data.
   - **View:** saved query that presents data.
   - **Volume:** governed file storage.
6. Unity Catalog controls who can discover and access those assets.

### The simplest way to remember

```text
Incoming data:
CSV / Excel / JSON / Parquet / Database / API / PDF
                         |
                         v
              Actual storage:
             Cloud object storage
                         |
                         v
             Databricks processing
                         |
                         v
              Delta tables / files
                         |
                         v
                 Unity Catalog
                         |
                         v
       Metastore -> Catalog -> Schema
                         |
                         v
                Tables / Views / Volumes
```
