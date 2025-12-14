# That’s Just My Cup of Tea: Configuring Cilium for Performance and Scale - Liz Rice & Neha Aggarwal

https://www.youtube.com/watch?v=yKPNmhckJHY

# Executive Summary
Cilium's default configuration **prioritizes compatibility over performance**. Production deployments require active tuning across two critical layers:
- Control Plane — Reduce API server and agent load at scale
- Data Plane — Minimize packet processing overhead and network latency

# Control Plane Optimization Solutions

## Problem

At scale (1k+ nodes), Cilium generates one CRD endpoint per pod, causing each agent to watch all cluster endpoints.  
**Result:** massive API server pressure and watch event storms during deployments.

---

## Solution A: Cilium Endpoint Slice (CES)

Batches multiple pod endpoints into intelligent slices based on deployment.

- **87% reduction** in API server latency
- **60% improvement** in pod network provisioning SLA
- **Available:** Cilium v1.16+
- **Status:** Stable and production-ready

---

## Solution B: Label Exclusion for Security Identities

Cilium generates security identities for every label on pods.

- **Problem:** High-churn labels (timestamps, UIDs) create unnecessary agent load
- **Solution:** Exclude labels not used for network policies

**Impact:** Reduced CPU/memory consumption on Cilium agents  
**Configuration:** Dynamic and flexible per-label filtering

---

## Solution C: Hubble Dynamic Metrics Filtering

- **Previous approach:** collect all observability metrics, then filter downstream
- **New approach:** filter at source based on namespace and labels
- Only collect DNS, TCP, HTTP metrics needed for specific workloads

**Impact:** Significant reduction in Prometheus/VictoriaMetrics scrape load

---

# 🚀 Data Plane Performance Solutions

## The Problem: Double Network Stack Traversal

Traditional container networking forces every packet through the host network stack twice:

- **Ingress:**  
  Physical interface → host stack → virtual Ethernet → pod namespace stack → application

- **Egress:**  
  Application → pod namespace stack → virtual Ethernet → host stack → destination

---

## Solution A: eBPF Host Routing

**Mechanism:** `BPF_redirect_peer` helper function intercepts packets at host namespace boundary.

- **Ingress:** directs packets directly to pod namespace, bypassing host stack
- **Egress:** looks up destination and redirects without full stack traversal

**Trade-off:** Still traverses virtual Ethernet with potential queuing/TCP back-pressure  
**Performance:** Significantly closer to native host-to-host throughput

---

## Solution B: Netkit Devices (Emerging Technology)

**Replacement:** Replaces virtual Ethernet with Netkit device pairs.

- **Key advantage:** host can manipulate eBPF programs inside pod namespace
- **Result:** eliminates virtual Ethernet connection entirely
- **Queuing:** no per-CPU queuing or TCP back-pressure
- **Performance:** parity with host networking (both throughput AND latency)

**Kernel requirement:** Linux 6.8+ (not yet standard in production)  
**Future:** Expected to become default for maximum performance

---

## Solution C: BIG TCP

- **Concept:** handle larger network packets (>64KB)
- **Benefit:** fewer packets = less processing overhead

**Impact:** Reduces CPU utilization for network processing  
**Requirement:** NIC driver support

---

# ⚠️ Critical Considerations

## Kernel Support Dependencies

| Feature          | Kernel Requirement | Production Readiness   |
|------------------|-------------------|------------------------|
| Netkit devices   | 6.8+              | Early adoption phase   |
| eBPF host routing| Recent kernel     | More widely available  |
| BIG TCP          | Depends on NIC    | Partial support        |

---

## Disruptive Change Management

- **New clusters:** can safely enable all features
- **Existing clusters:** configuration changes may disrupt active connections

**Recommendation:** Plan changes during maintenance windows.

---

## Workload-Specific Tuning

No single configuration optimizes all scenarios. Performance depends on:

- Traffic type (streaming vs. request-response)
- Packet size
- Encryption requirements
- Throughput vs. latency priorities

---

# 🔧 Validation & Testing

**Built-in tool:** `cilium connectivity perf` CLI command

**Measures:**

- Pod-to-pod same node
- Pod-to-pod cross node
- Pod-to-host bidirectional
- Throughput (Mbps) and latency/response times

**Best Practices:**

- Run multiple times to establish statistical baselines
- Calculate P99 and averages (not single runs)
- Compare before/after optimization changes

---

# ✅ Key Takeaways for Production

- **Immediate Action:** Enable Cilium Endpoint Slice on clusters with 1k+ nodes — dramatic control plane improvement with zero compatibility concerns
- **Label Audit:** Review and exclude high-churn labels from security identity generation to reduce agent overhead
- **Observable at Scale:** Implement Hubble dynamic metrics filtering to observe large clusters without overwhelming monitoring infrastructure
- **eBPF Host Routing:** Enable on existing clusters if kernel supports it — significant data plane improvement without connection disruption
- **Netkit Planning:** Monitor kernel adoption; plan Netkit migration for new clusters when Linux 6.8+ becomes standard
- **Baseline First:** Establish performance metrics with `cilium connectivity perf` before making configuration changes
- **Default Philosophy:** Understand that Cilium's defaults prioritize compatibility over performance — production requires active optimization decisions
- **Workload Analysis:** Different applications require different tuning — container networking, request-response services, and streaming workloads each have distinct optimal configurations
- **Change Planning:** Avoid disruptive reconfigurations on existing clusters with active connections — plan major changes during maintenance windows

# References:
- https://github.com/cilium/design-cfps/blob/main/cilium/CFP-36975-configuration-profiles.md



