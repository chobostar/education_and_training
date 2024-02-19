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
