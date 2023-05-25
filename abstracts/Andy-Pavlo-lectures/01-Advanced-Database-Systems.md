# Advanced Database Systems

[Advanced Database Systems (Spring 2020)](https://www.youtube.com/playlist?list=PLSE8ODhjZXjaKScG3l0nuOiDTTqpfnWFf)

#### Background

Much of the development history of DBMSs is about dealing with **the limitations of hardware**.

The idea is same, limitations are not same.
- slower disks
- single-core CPU
- RAM was limited

Modern:
- DRAM
- Structured data sets are smaller

How to avoid bottlenecks of Disk-Oriented DBMSs:
- the primary storage is non-volatile storage - HDD, SSD
- fixed-length pages (aka blocks)
- in-memory buffer pool to cache pages
  - copy from disk into a frame in its buffer pool
  - no free frames -> page evict
  - evicted page is dirty -> write it back to disk

In-memory DBMSs 
- what if we give DBMS a lot of memory?

Concurrency Control Bottlenecks
- set locks to provide ACID
- locks are stored in a separate data structure

Logging and recovery
- all modifications have to be flushed to the WAL before a txn can commit

Disk-Oriented DBMS Overhead (CPU Instructions)
- Buffer pool (34%)
- Latching (14%)
- Locking (16%)
- Logging (12%)
- B-tree keys (16%)
- Real work (7%)

In-memory DBMSs
- DRAM prices are low and capacities are high
- Data organizations
  - tuples in blocks/pages
    - direct memory pointers vs record ids
    - fixed-length vs variable-length data pools
    - use checksums to detect software errors from trashing the database
- Query processing
  - seqscans are no longer faster
- still needs a WAL on non-volatile storage
  - use group commit to amortize fsync cost
- bottlenecks
  - lockings/latching
  - cache-line misses
  - pointer chasing
  - predicate evaluations
  - data movement & copying
  - networking (between application & DBMS)

concurrency control schemas
- 2PL
  - lock (shared, exclusive)
  - deadlock detection
    - each txn maintains a queue of the txns that hold the locks that if waiting for
- timestamp ordereing (t/o)
  - basic t/o
    - check for conflict on each read/write
    - copy tuples on each access to ensure repatable reads
  - optimistic currency control (OCC)
    - store all changes in private workspace
    - check for conflicts at commit time and then merge
  - observation
    - low contension -> optimistic protocols perform better
    - high contention -> degenerate

bottlenecks
- lock thrashing
  - DL_DETECT, WAIT_DIE
- timestamp allocation
  - All t/o algorithms + WAIT_DIE
- memory allocations
  - OCC + MVCC
 
#### Modern Analytical Database Systems
https://www.youtube.com/playlist?list=PLSE8ODhjZXjYzlLMbX3cR0sxWnRM7CLFn

Storage:
- Columnar storage
- Compression
- Indexes

Query Execution:
- Processing Models
- Scheduling
- Vectorization
- Compilation
- Joins
- Materialized Views

Query Optimization

Network Interfaces

Client-Interface -> Optimization -> Query Execution -> Storage

Distributed query execution
- query plan is a DAG of physical operators

(in high-level the same as on as single-node DBMS)


Worker nodes:
- cpu / memory / disk
- contains persistence data (e.g. some files)
  - doesn't matter local data or shared

workers -> Shuffle nodes (optional, has a lot of memory) -> Workers -> Final result

nothing diff from a single node for distributed query execution

communation thought network

Data categories
- Persistent Data
  - the "source of record" for the db (tables)
  - assume that these data files are immutable, but can support updates by rewriting them
- Intermediate Data
  - short-lived artifacts produced by query operators during execution and then consumed by others
  - the amount of data has no correlation to amount of persistent data


Distributed system architecture

- specifies the location of the db's persistent data files. This affects how nodes coordinate with each other
- two approaches (not mutually exclusive):
  - push query to data
    - send the query (or a portion of it) to the node that contains the data
      - when transfer cost is so high
  - pull data to query
    - bring the data to the node that is executing a query that needs it for processing
    - this is necessary when there is no compute resources available where persistent data files are located


Shared nothing
- each DBMS instance has its own cpu / memory / locally-attached disk
- database is parittioned into disjoint subsets across nodes
- since data is local, the DBMS can access it via POSIX API

Shared disk
- each node accesses a single logical disk via an interconnect, but also have their own private memory and ephemeral storage
  - must send messages between nodes to learn about their current state

Instead of a POSIX API, the DBMS accesses disk using a userspace API


System architecture
- choice #1: shared nothing
  - harder to scale capacity (data movement)
  - potentially better perf & effeciency
  - apply filters where the data resides before transferring
- choise #2: shared disk
  - scale compute layer independently from the storage layer
  - easy to shutdown idle compute layer resources
  - may need to pull uncached persistent data from storage layer to compute layer before applying filters

Shared disk
- traditionally the storage layer in shared-disk DBMSs where dedicated on-prem NAS.
  - Example: Oracle Exadata
- cloud object stores are now the prevailing storage target for modern OLAP DBMSs because they are "infinitely" scalable
  - Examples: Amazon S3, Azure Blob, Google Cloud Storage

Object stores
- partition the database's tables (persistent data) into large, immutable files stored in an object store.
  - all attributes for a tuple are stored in the same file in columnar layour (PAX)
- the DBMS retrieves a block's header to determine what byte ranges it needs to retrive (if any).
- each cloud vendor provides their own proprietary API to access data (PUT, GET, DELETE)
  - some vendors support predicate pushdown (S3)

Observation
- snowflake is a monolithic system comprised of components built entirely in-house
- but this means that multiple organizations are writing the same DBMS software

OLAP commoditization
- one recent trend of the last decade is the breakout OLAP engine sub-systems into standalone open-source components
  - this is typically done by organizations not in the business of selling DBMS software
- examples
  - system catalogs
  - query optimizers
  - file format / access libraries
  - execution engines

System catalogs
- a DBMS tracks a database's schema (tables, columns) and data files in its catalog
- notable implementations
  - HCatalog
  - Google Data Catalog

Query optimizers
- extendible search engine framework for heuristic and cost-based query optimization
  - provides transformation rules and cost estimates
- this is the hardest part to build in any DBMS
- examples
  - Greenplum Orca
  - Apache Calcite

File formats
- most DBMMs use a proprietary on-disk binary file format for their db. The only way to share data between systems is to convert data into a common text-based format
  - CSV, JSON, XML
- there are open-source binary file formats that make it easier to access data across systems and libraries for extracting data from files
  - they provide an iterator interface to retrieve (batched) columns from files

Unverslal formats
- apache parquet
- apache iceberg
- apache ORC
- HDF5
- apache CarbonData
- Apache Arrow

Execution engines
- standalone libraries for executing vectorized query operators on columnar data
  - input is a DAG of physical operators
  - require external scheduling and orchestration
- examples
  - Velox
  - DataFusing
  - Intel OAP

Conclusing
- about understanding the high-level context of what modern OLAP DBMs look like

#### Storage Models and Data layout

Obesvation
- the lowest physical representation of data in a database
- what data "looks" like determines almost a DBMS entire system architecture
  - processing model
  - tuple materialization strategy
  - operator algorithms
  - data ingestion / updates
  - concurrency control
  - query optimization

storage models -> type representation -> partitioning

storage models
- specifies how it physically orginizes tuples on disk and in memory
  - choice #1: N-ary Storage model (NSM)
  - choice #2: Decomposition Storage Model (DSM)
  - choice #3: Hydrid storage model (PAX)

N-ary storage model (NSM)
- the DBMS stores all the attributes for a single tple contiguosly in a single page
- ideal for OLTP workloads where txns tend to access individual entities and insert-heavy workloads
  - use the tuple-at-a-time iterator processing model
- NSM database page sizes are typically some constant multiple of 4 KB hardware pages
  - example: Oracle (4 KB), Postges (8 KB), Mysql (16 KB)

NSM: Physical organization
- a disk-oriented NSM system stores a tuple's fixed-lenght and variable-lenth attributes contiguously in a single slotted page
- the tuple's record id (paga #, slot #) is a how the DBMS uniquely identifies a physical tuple

N-ary storage model (NSM)
- advantages
  - fast inserts, update and deletes
  - good for queries that need the tipe tuple (OLTP)
  - can use index-oriented physical storage for clustering
- disadvantages
  - not good for scanning large portions of the table and/or a subset of the attributes
  - terrible memory locality in access patterns
  - not ideal for compressin because of multiple value domains within a single page


Decompositing storage model (DSM)
- the DBMS stores a single attribute for all tuples contiguously in a block of data
- ideal for OLAP workloads where read-only queries perform large scans over a subset of the table' attributes
  - use a batched vectorized processing model
- file sizes are larger (100s of MBs), but it may still orginize tuples within the file into smaller group

DSM: Physical organization
- store attributes and meta-data in separate arrays of fixed-lenght values
- maintain a **separate file per attribute** with a dedicated header are for metadata about entire column

DSM: Tuple identification
- choice #1: fixed-lenght offsets
- choice #2: embedde tuple IDs

(if there is no data "null bitmaps" are used and space is still reserved)

DSM: Variable-length data
- padding variable-length fields to ensure they are fixed-length is wasteful, especially for large attributes
- a better approach is to use dictionary compressing to convert repetitive variable-length data into fixed-length values (typically 32-bit integers)

DMS: System history
- 1990s: SybaseIQ (in-memory only)
- 2000s: Vertica, Vectorwise, MonetDB
- 2010s: Everyone (Redshift, Clickhouse etc etc)

Decomposition storage model (DSM)
- Advantages
- Reduces the amount of wasted I/O per query because the DBMS only reads the data that it needs
- Faster query processing because of increased locality and cached data reuse
- Better data compression
- Disadvantages
- Slow for point queries, inserts, updates and deletes because of tuple splitting/stitching/reorganization

Observation
- OLAP queries almost never access a single column in a table by itself
- But we still need to store data in a columnar format to get the storage + execution benefits
- We need columnar scheme that still stores attributes separately but keeps the data for each tuple physically close to each other


PAX storage model
- partition attributes across (PAX) is a hydrib storage model that vertically partitions attributes within a database page
  - this is what Paraquet and Orc use
- the goal is to get the benefit of faster processing on columnar storage while retaining the spatial locality benefits of row storage

PAX: Physical organization
- horizontally partition rows into groups. then vertically partition their attributes into columns
- global header contains directory with the offsets to the file's row groups
  - this is stored in the footer if the file is immutable
- each row group contains its own meta-data header about its contents

Memory pages:
- An OLAP DBMS uses the buffer pool manager methods
- OS maps physical pages to virtual memory pages
- the CPU's MMU maintains a TLB that contains the physical address of a virtual memory page
  - the TLB resides in the CPU caches
  - It cannot obviously store every possible entry for a large memory machine
- when you allocate a block of memory, the allocator keeps that it aligned to page boundaries

Transparent huge pages (THP)
- greatly reduces of number of TLB entries
- with THP, the OS reorganizes pages in the background to keep things compact
  - split larget pages into smaller pages
  - combine smaller pages into larger pages
  - can cause the DBMS process to stall on memory access
- historically, every DBMS advices you to disable this THP on linux
- recent research from Google suggests that HP improved their data center workload by 7%

Data representation
- ...

Null data types
- choice #1: special values (design a value or represent NULL for a data type (e.g. INT32_MIN)
- choice #2: null column bitmap header
- choice #3: per attribute null flab
- store a flag that marks that a value is null
- must use more space than just a single bit

Observation
- data is "hot" when it enters the database
  - a newly inserted tuple is more likely to be updated again the near future
- as a tuple ages, it is updated less frequently
  - at some point, a tuple is only accessed in read-only queries along with other tuples

Hydrid storage model
- use separate execution engines that are optimized for either NSM or DSM databses
  - store new data in NSM for fast OLTP
  - migrate data to DSM fore more efficient OLAP
  - combine query results from both engines to appear as a single logical datases to the application
- choice #1: fractured mirrors
- choice #2: delta store

Fractured mirrors
- store a second copy of the database in a DSM layout that is automatically updated
  - all updates are first entered in NSM then eventually copied into DSM mirror
  - if the DBMS supports updates, it must invalidate tuples in the DSM mirror

Delta store
- stage updates to the database in an NSM table
- a background thread migrates updates from delta store and applies them to DSM data
  - batch large chunks and then write them out as a PAX file

Database partitioning
- Split database across multiple resources
  - disks, nodes, processors
  - often called "sharding" in NoSQL systems

The DBMS executes query fragments on each partition and then combines the results to produce a single answer.

The DBMS can partition a database physically (shared nothing) or logically (shared disk).

Horizontal partitioning
- split a table's tuples into disjoint subsets based on some partitioning key and scheme
  - choose column(s) that divides the database equally in terms of size, load, or usage

Partitioning schemes:
- hashing
- ranges
- predicates

Parting thoughts
- every modern OLAP system is using some variant of PAX storage. The key idea is that all data must be fixed-length
- real-world tables contain mostly numeric attributes (int/float), but their occuped storage is mostly comprised of string data
- modern columnar systems are so fast that most people do not  denormalize data warehouse schemas