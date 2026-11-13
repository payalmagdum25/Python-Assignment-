# Unity Catalog

Unity Catalog is the **data governance and organisation layer** in Databricks.

When a company receives data from different sources, it needs a proper way to organise that data, control who can access it, and manage it. Unity Catalog helps with this.

**Important:**

Unity Catalog is not the place where all the actual data files are physically stored. It mainly manages the metadata and access to the data.

The actual data is generally stored in cloud storage such as:
- AWS S3
- Azure Data Lake Storage (ADLS)
- Google Cloud Storage (GCS)

---

## 1. Metastore

A metastore is the **top-level container** in Unity Catalog.

It is the main place where Unity Catalog keeps information about the data objects and how they are managed.

For example, the metastore keeps metadata such as:

- Names of catalogs, schemas, tables, views and volumes.
- Table columns and data types.
- Where the actual data is stored.
- Who has permission to access a particular object.
- Storage credentials and external locations.
- Information used for data lineage and governance.

**What is Metadata?**

Metadata means information about the data. It is not necessarily the actual rows or contents of the files.

**Does the metastore store the actual data?**

No. The metastore mainly stores and manages metadata.

In simple words:

- **Cloud Storage:** The place where the actual files/data are kept.
- **Unity Catalog Metastore:** The place that manages information and permissions for those data objects.

---

## 2. Catalog

A catalog is the **next level inside a metastore**.

It is used to group related schemas. Usually, catalogs are created based on business areas, environments or projects.

For example, a company may create:

- `hr_catalog`
- `finance_catalog`
- `sales_catalog`

The HR catalog can contain employee-related data, the Finance catalog can contain payment and budget data, and the Sales catalog can contain customer and order data.

A catalog is an organisation level. It does not mean that all the data is physically stored inside the catalog.

---

## 3. Schema

A schema is created inside a catalog.

It is used to organise tables, views, volumes and other objects into smaller groups.

For example, inside `hr_catalog`, we can create:

- `employee`
- `payroll`
- `recruitment`

The employee schema may contain employee details, the payroll schema may contain salary information, and the recruitment schema may contain candidate information.

Schemas help keep related objects together and make the data easier to manage.

---

## 4. Tables

A table is used to store structured data in rows and columns.

For example, an employee table can look like this:

| Employee_ID | Name | Department | Salary |
|---|---|---|---|
| 101 | Rahul | IT | 45000 |
| 102 | Priya | HR | 40000 |
| 103 | Amit | Finance | 50000 |

---

## 5. Views

A view is a saved query based on one or more tables or other views.

A view usually does not store a separate copy of all the result data.

When we query the view, Databricks uses its saved query definition to retrieve the result from the underlying data.

---

## 6. Volumes

A volume is used to organise and provide governed access to files that are not being managed as table data.

For example, a company may have:

- PDF employee documents
- Resume files
- Images
- Audio files
- CSV files received from another system
- Text documents
- JSON files

These files can be accessed through a Unity Catalog volume.

A volume is useful when we want to store, organise, read or write files using a governed location.

**What file formats can a volume contain?**

A volume can contain many types of files. It is not restricted to one particular format.
