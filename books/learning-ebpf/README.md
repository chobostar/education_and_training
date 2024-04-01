# Learning eBPF

- https://www.parca.dev/
- https://github.com/lizrice/learning-ebpf

## CHAPTER 1. What Is eBPF, and Why Is It Important?

Just a few of the things you can do with eBPF include:
• Performance tracing of pretty much any aspect of a system
• High-performance networking, with built-in visibility
• Detecting and (optionally) preventing malicious activity

- The ability to attach eBPF programs to kprobes was added in 2015
- The year 2020 saw the introduction of LSM BPF, allowing eBPF programs to be attached to the Linux Security Module (LSM) kernel interface.

```bash
strace -c echo "hello"
```

eBPF programs can collect information
about all manner of events across a system, and they can use complex, customized
programmatic filters to send only the relevant subset of information to user space

eBPF programs in the kernel have visibility of all applications running on a Kubernetes node:
- We don’t need to change our applications, or even the way they are configured, to instrument them with eBPF tooling
- As soon as it’s loaded into the kernel and attached to an event, an eBPF program can start observing preexisting application processes

the sidecar approach has a few downsides:
- The application pod has to be restarted for the sidecar to be added
- Something has to modify the application YAML. This is generally an automated process, but if something goes wrong, the sidecar won’t be added, which means the pod doesn’t get instrumented.
- When there are multiple containers within a pod, they might reach readiness at different times, the ordering of which may not be predictable. Pod start-up time can be significantly slowed by the injection of sidecars, or worse, it can cause race conditions or other instabilities
- Where networking functionality such as service mesh is implemented as a side‐
  car, it necessarily means that all traffic to and from the application container has
  to travel through the network stack in the kernel to reach a network proxy con‐
  tainer, adding latency to that traffic;

network security implemented in eBPF can police all traffic on the host machine,

## CHAPTER 2. eBPF’s “Hello World”


CAP_BPF was introduced in kernel version 5.8, and it gives sufficient
privilege to perform some eBPF operations like creating certain
types of map. However, you will probably need additional
capabilities:
- CAP_PERFMON and CAP_BPF are both required to load tracing programs.
- CAP_NET_ADMIN and CAP_BPF are both required for loading networking programs.

As soon as the hello eBPF program is loaded and attached to an event, it gets trig‐
gered by events that are being generated from preexisting processes.
- eBPF programs can be used to dynamically change the behavior of the system
- There’s no need to change anything about other applications for them to be visible to eBPF.

the `bpf_trace_printk()` helper function in the kernel always sends output to the same predefined pseudofile
location: `/sys/kernel/debug/tracing/trace_pipe`

### BPF Maps

A map is a data structure that can be accessed from an eBPF program and from user
space:
- User space writing configuration information to be retrieved by an eBPF program
- An eBPF program storing state, for later retrieval by another eBPF program (or a future run of the same program)
- An eBPF program writing results or metrics into a map, for retrieval by the user space app that will present results

### Hash Table Map

BCC’s version of C is very loosely a C-like language that BCC rewrites before it sends the
code to the compiler. BCC offers some convenient shortcuts and macros that it converts into “proper” C.

### Perf and Ring Buffer Maps

Ring Buffer - a piece of memory
logically organized in a ring, with separate “write” and “read” pointers. Data of some
arbitrary length gets written to wherever the write pointer is, with the length informa‐
tion included in a header for that data. The write pointer moves to after the end of
that data, ready for the next write operation.

data gets read from wherever the read pointer is, using
the header to determine how much data to read. The read pointer moves along in the
same direction as the write pointer so that it points to the next available piece of data.

If the read pointer catches up with the write pointer, it simply means there’s no data to
read. If a write operation would make the write pointer overtake the read pointer, the
data doesn’t get written and a **drop counter** gets incremented. Read operations include
the drop counter to indicate whether data has been lost since the last successful read.

### Function Calls

in the early days, eBPF programs were not permitted to call functions other than helper functions

“always inline” their functions, like this:
```
static __always_inline void my_function(void *ctx, int val)
```

### Tail Calls

tail calls can call and execute another eBPF program and
replace the execution context, similar to how the execve() system call operates for
regular processes.