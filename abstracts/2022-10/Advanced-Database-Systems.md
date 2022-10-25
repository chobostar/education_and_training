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
 