
# Compute Plane

The compute plane is the part of Databricks where the actual data processing takes place.

When we run a notebook, SQL query or job, computing resources are required to execute the operations. The compute plane provides those resources.

It includes the driver and the workers. Executors run on worker nodes to process data.

**In simple words:**

- Unity Catalog helps organise and govern data.
- The compute plane provides the resources to process that data.

---

## 1. Driver

The driver is the main coordinating process of a Spark application.

It is responsible for:

- Running the main application code.
- Creating and managing the Spark execution plan.
- Coordinating the execution of jobs, stages and tasks.
- Scheduling tasks on executors.
- Tracking the progress of tasks.
- Receiving results when required.

**Example:**

Suppose we have 10 lakh employee records and want to calculate department-wise salary.

The driver understands the operation, plans the work, divides it into tasks and schedules those tasks for execution.

The driver coordinates the work; it does not normally process all the distributed data by itself.

---

## 2. Worker

A worker is a machine or compute node that provides resources for processing data.

Workers are used to run the actual distributed computation.

A Spark cluster can have multiple workers. Each worker provides resources such as CPU and memory.

For example:

- Worker 1 processes some employee data.
- Worker 2 processes another part.
- Worker 3 processes another part.

Workers allow Spark to process different partitions in parallel.

---

## 3. Executor

An executor is a process that runs on a worker node and performs the tasks assigned by the driver.

It is responsible for:

- Executing tasks.
- Processing data partitions.
- Keeping data in memory or on disk when needed.
- Sending task results and status information back to the driver.

A worker is the machine. An executor is the process running on that machine.

A worker can run one or more executors, depending on the cluster configuration and available resources.

---

## 4. Simple Real-Life Example

Imagine a company has a manager and three office rooms where employees work.

- **Manager = Driver**
- **Office rooms = Workers**
- **Employees working in those rooms = Executors** (a simplified analogy)
- **Individual assigned work = Tasks**

The manager plans and assigns work. The employees perform the work using the resources available in their rooms.

In Spark, the driver schedules tasks to executors, and executors run those tasks on worker nodes.

---

## 5. Compute Plane Architecture

```text
                 DRIVER
        (Coordinates the application)
                    |
          Schedules tasks to executors
                    |
       +------------+------------+
       |            |            |
       v            v            v
    WORKER 1     WORKER 2     WORKER 3
       |            |            |
    Executor     Executor     Executor
       |            |            |
     Tasks        Tasks        Tasks
       |            |            |
   Partition 1  Partition 2  Partition 3
```

