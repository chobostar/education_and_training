## Analytical Database Indexes

https://www.youtube.com/watch?v=lGRAq98ejWs&list=PLSE8ODhjZXjYzlLMbX3cR0sxWnRM7CLFn&index=4

If the DBMS assumes that its data files are immutable, it enables several optimization opportunities

Observation
- OLTP DBMSs use indexes to find individual tuples without performing sequental scans
  - tree-based indexes (B+trees)
  - also need to accomodate incremental updates
- But OLAP queries don't necessarily need to find individual tuples and data files are read-only

How can we speed up seq scans?

Sequential Scan optimizations
- data prefetching
- task parallelization / multi-threading
- clustering / sorting
- late materialization
- materialized views / result caching
- data skipping
- data parallelization / vectorization
- code specialization / compilation

Data skipping
- approach #1: approximate queries (lossy)
  - execute queries on a sampled subset of the entire table to produce approximate results
  - examples: BlinkDB, Redshift, Google BigQuery, Snowflake...
- approach #2: data pruning (loseless)
  - use auxiliary data structures for evaluating predicates to quickly identify portions of a table that the DBMS can skip instead of examining tuples individually
  - DBMS must consider trade-offs between scope vs filter efficacy, manual vs automatic

Data pruning (loseless):
- predicate selectivity
  -  how many tuples will satisfy a query's predicates
- skewness
  - whether an attribute has all unique values or contain many repeated values
- clustering / sorting
  - whether the table is pre-sorted on the attributes accessed in a query's predicates

Zone maps
- pre-computed aggregates for the attribute values in a block of tuples. DBMS checks the zone map first to decide whether it wants to access the block
  - originally called Small materialized aggregates (SMA)
  - DBMS automatically creates/maintains this meta-data

Observation
- trade-off between scope vs filter efficacy
  - if the scope is too large, then the zone maps will be useless
  - if the scope is too small, then the DBMS will spend too much checking zone maps
- zone maps are only useful when the target attribute's position and values are correlated

Bitmap indexes
- store a separate Bitmap for each unique value for an attribute where an offset in the vector corresponds to a tuple
  - the i-th position in the Bitmap corresponds to the i-th tuple in the table
- typically segmented into chunks to avoid allocating large blocks of contiguous memory
  - example: one per row group in PAX

Bitmap index: design choices
- encoding scheme
  - how to represent and organize data in a Bitmap
    - encoding approaches
      - approach #1: equality encoding
        - basic scheme with one bitmap per unique value
      - approach #2: range encoding
        - use one bitmap per interval instead of one per value (Postgres BRIN)
      - approach #3: hierarchical encoding
        - use a tree to identify empty key ranges
      - approach #4: bit-sliced encoding
        - use a bitmap per bit location across all values
- compression
  - how to reduce the size of sparse Bitmaps

