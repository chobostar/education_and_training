# Introduction to Cilium

https://isovalent.com/resource-library/labs/

https://isovalent.com/learning-tracks

eBPF based

Has Build-in
- Ingress L7
- Hubble - Observability
- Tetragon - Security

Cilium:
- natively understands container identities
- parses API protocols like HTTP, gRPC, and Kafka
- and provides visibility and security that is both simpler and more powerful than traditional approaches

Hubble is an open source software and is built on top of Cilium and eBPF to enable deep visibility into:
- the communication and behavior of services as well as
- the networking infrastructure in a completely transparent manner

The kernel has visibility across the entire system and is highly performant, but needs to provide a stable interface to applications, so it lacks the flexibility of user space programming.

- updates to the kernel can take years to reach end users
- It is possible to extend the kernel’s functionalities by writing and loading kernel modules

eBPF is an event-driven architecture that runs specific programs when the kernel or an application passes a certain hook point.

eBPF programs can be loaded and upgraded in real time without the need to restart the kernel.

The Linux kernel expects eBPF programs to be loaded in the form of bytecode. Typically, eBPF developers write
programs in C, Rust, or other languages, which are then compiled into eBPF bytecode. eBPF programs can be
loaded into the Linux kernel using the bpf() system call, directly or through one of the available eBPF libraries. 

The Just-in-Time (JIT) compilation step translates the generic bytecode of the program into the machine-specific
instruction set to optimize execution speed. This makes eBPF programs run as efficiently as natively compiled kernel
code or as code loaded as a kernel module.

Users can leverage the following objects or mechanisms when programming with eBPF:
- Share collected information, retrieve configuration options, and store state through eBPF maps to save and retrieve
  data in a wide set of data structures. These maps can be accessed from eBPF programs as well as from applications
  in user space.
- eBPF programs can make function calls into a set of dedicated kernel functions (eBPF helpers/kfuncs) to help them
  accomplish some specific tasks
- For more flexibility, eBPF programs are also composable with the concept of tail and function calls.
- Various mechanisms allow eBPF programs to contain loops, while ensuring the programs always terminate.

eBPF enhances networking by enabling efficient packet processing and filtering in the kernel

Attaching eBPF programs to trace points as well as kernel and user application probe points gives powerful introspection
abilities for the kernel and user space applications and useful insights to troubleshoot system performance problems.


