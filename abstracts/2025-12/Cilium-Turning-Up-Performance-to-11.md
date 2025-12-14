# Turning up Performance to 11: Cilium, NetKit Devices, and Going Big with TCP
https://kccncna2023.sched.com/event/1R2s5

## Executive Summary

The talk presents a systematic engineering journey to eliminate container networking overhead entirely. Starting from a **37% performance loss** (63 Gbit/s vs 100 Gbit/s host baseline), Daniel Borkmann documents how seven major kernel features and Cilium's orchestration layer enable Pod networking to achieve **bare-metal performance with zero overhead**. This is accomplished **without** requiring application rewrites or network topology changes.

---

## 🔧 The Core Problem: Why Container Networking Is Slow

### Three Critical Bottlenecks

1. **Kube-Proxy Scalability**
    - Linear walk through service tuples creates performance cliff
    - Becomes prohibitively expensive with hundreds of services
    - Cannot be replaced due to netfilter dependencies

2. **Routing Through Upper Stack**
    - Packets forced through IP, netfilter, and routing layers
    - Adds latency and CPU overhead
    - Unnecessary processing for known routes

3. **TCP Backpressure Breakage (The Hidden Killer)**
    - netfilter's `TPROXY` helper calls `skb_orphan()` — telling TCP stack the packet left the node
    - But the packet hasn't actually left yet — it's still in host namespace
    - TCP stack thinks it can push more data, evading socket send buffer (`SO_SNDBUF`) limits
    - **Results:** excessive queuing, retransmits, packet drops

---

## 🚀 The Solution: Seven Building Blocks (2019–2024)

### Building Block #1: BPF Kube-Proxy Replacement

- **Status:** Deployed
- **Benefit:** Eliminates linear service lookup overhead

Replaces kube-proxy entirely with eBPF programs:

- **North-South:** Per-packet NAT at `tc` BPF layer (on physical interface)
- **East-West:** Per-`connect(2)` at socket layer, backend selection at connection time

**Features:**

- Maglev hashing
- HostPort support

**Result:** No netfilter dependency, predictable performance scaling.

---

### Building Block #2: XDP-Based Service Load-Balancer

- **Status:** In production (seznam.cz case study)

High-performance L4 load balancer at the driver level:

- Processes packets **before** reaching the OS
- Covers all Kubernetes service types

**Production example:**

- One node with XDP handling traffic previously split across IPVS-backed nodes
- Achieved with **minimal CPU usage**

**Supports:**

- Maglev
- DSR (Direct Server Return)

---

### Building Block #3: Bandwidth Manager (fq/EDT/BBR)

- **Status:** Deployed
- **Problem Solved:** Scalable egress rate-limiting with minimal latency impact

**Mechanism:**

- Agent sets up **multi-queue (multiq)** on transmit side
- **Fair Queue (FQ)** scheduler in kernel
- BPF program computes **packet departure time** based on Pod's bandwidth limit
- Lockless rate limiting (no locks = better scalability)

**Performance:**
- **4.2x better P99 latency** vs traditional Hierarchical Token Bucket (HTB)

#### BBR Congestion Control Integration (Kernel 5.18)

- Google's BBR uses different congestion signals than default CUBIC
- **Previous problem:** delivery timestamps cleared when crossing network namespaces
- **Solution:** Fix by Martin Lau + Daniel Borkmann preserving timestamps

**Real impact demo (KubeCon EU 2022):**

- Video streaming over lossy network
- **BBR + BPF:** Stayed in HD (high definition)
- **CUBIC (default):** Dropped to low resolution

---

### Building Block #4: BPF Host Routing

- **Status:** Deployed (Kernel 5.10)
- **Problem:** Bypass the entire upper stack for routing

Two new BPF helpers:

#### `bpf_redirect_peer()` — Ingress Direction

- Fast namespace switch from physical device to veth peer
- Stays in same processing context (no context switch)
- Avoids per-CPU backlog queuing (**critical for latency**)
- **Performance:** 63 Gbit/s → 90 Gbit/s

#### `bpf_redirect_neigh()` — Egress Direction

- Injects packet into L2 neighbor subsystem
- FIB lookup + dynamic MAC address resolution
- **CRITICAL:** Does **not** call `skb_orphan()` — **fixes TCP backpressure**
- Retains socket context (`skb->sk`) until reaching physical NIC Qdisc

**Combined Impact:** 63 Gbit/s → 90 Gbit/s (still ~10% gap remaining)

---

### Building Block #5: TCX (TC Express) — Modern BPF Datapath

- **Status:** Released with Linux 6.6+
- **Effort:** ~1 year rework
- **Problem:** Original `tc` BPF (from 2015) architecturally outdated

#### What Changed

**Old `tc` BPF architecture:**

- Used fake qdisc + `cls_bpf` for attachment
- Inefficient entry point (~59 CPU cycles)
- No BPF link support (fragile)
- Linked-list based (poor cache locality)

**New `tcx` architecture:**

- Array-based multi-program framework (`bpf_mprog`)
- ~33 CPU cycles entry point (**44% faster**)
- BPF link support (robust control plane)
- Before/After dependency directives
- Common “look-and-feel” across all attach points

**Future:** Integrate `bpf_mprog` into XDP and other attach points for consistent API.

---

### Building Block #6: Netkit Devices — Veth Replacement

- **Status:** Linux 6.7+, in production testing at Meta & Bytedance
- **Game Changer:** First time container networking matches bare-metal performance

#### The Veth Problem

- Virtual Ethernet pair inherently requires per-CPU backlog queuing
- Defers to `ksoftirqd` (context switch = latency)
- Cannot natively attach BPF in Pod namespace
- TCP backpressure issues remain

#### Netkit Solution

**Architecture:**

- **Primary device:** In host namespace (Cilium manages)
- **Peer device:** In Pod namespace
- **BPF integration:** Native to driver internals, not external attachment
- **Modes:** L3 (default) or L2

**Key Innovation:**

- Host can manipulate eBPF programs on both primary **and** peer devices
- Application cannot detach security policies
- BPF is integral to driver, not configurable from inside Pod

**Process Context Execution:**

- **veth:** Defers to `ksoftirqd` (scheduling latency)
- **netkit:** Remains in process context (better scheduler decisions, no context switch)

**Performance Impact:**

- **Throughput:** As high as host (100+ Gbit/s) ✓
- **Latency:** As low as host ✓

> First time in Kubernetes history: Pod networking overhead completely eliminated.

---

### Building Block #7: BIG TCP (IPv4 & IPv6)

- **Status:** Cilium 1.14+
- **Problem:** TCP packet size limit for 100G+ NICs

#### Historical Constraint

- GSO/GRO limit: **64KB** (constrained by 16-bit IP `total_len` field)
- For 1.5KB packets: ~40 packets needed to reach 64KB
- Means **40x per-packet processing overhead**

#### How BIG TCP Works

- Increases GSO/GRO upper limit to **192KB** (48 pages)
- TSO on NIC segments large packets at 192KB
- GRO reconstructs 192KB packets on receive
- Max TSO probing: Auto-adapts to driver capabilities
    - Example: Intel `ice` driver: 128KB

**Key Insight:**

- No network changes required
- Affects only local host GSO/GRO engine
- MTU unchanged
- Pure kernel optimization
- Deployed in Google's production fleet

#### Performance Gains

- **TCP_RR (request-response latency):** 2.2x lower P99
- **Throughput:** 42% more transactions/sec
- Intel `ice` driver reported: **+75% TCP_RR rate improvement**
