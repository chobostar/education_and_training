# Kubernetes Antipatterns: CPU Limits

https://www.youtube.com/watch?v=x9_9iaVszpM

- K8s scheduling
  - banch of pods to banch of nodes
  - moving pods between nodes is expensive
  - nodes have finite cpu that can't change
  - pods use chaning amounts of cpu
  - scheduling requires guessing about the future 
  - **fundamental dilemma**
    - **overutilization**
      - more efficient
      - cheaper
      - doesn't work under stress
    - **underutilization**
      - more reliable
      - more expensive
- CPU Requests
  - how much cpu this pod will use
  - no node is ever over-allocated
  - each node also has CPU reserved for the system itself which pods can't use
  - **Misconception #1: "Requests are only used for scheduling"**
    - CPU time are guaranteed
    - Excess CPU resources will be distributed based on the amount of CPU requested
- CPU Limits
  - an upper limit
  - **Misconception #2: "Limits do no harm as long as they're higher than your usage"**
    - CPU Usage graphs look different in different time periods. for example 5m, and 100ms periods 
- Best practices and misconceptions
  - Advise (Tim Hockin, Google)
    - 1) Always set memory limit == request
    - 2) Never set CPU limit
    - expect edge cases
      - perf testing
      - windows nodes
      - customers who benchmark you
  - **Misconception #3: "CPU and memory behave the same"**
    - CPU is compressible. It can be given and taken away
    - Memory is non-compressible. To take it away you need to kill the pod (OOM Kill).

Recommendations
- Define CPU requests for everything
- Assuming everything has somewhat accurate CPU requests, never define limits
- Monitor your requests periodically and make sure they're accurate
- For memory, always set request=limit and don't make it too low