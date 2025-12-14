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

## CHAPTER 3. Anatomy of an eBPF Program

Stages of ebpf program:
- C (or Rust) source code is compiled into eBPF bytecode, 
  which is either JIT-compiled or interpreted into native machine code instructions

bytecode runs in an eBPF virtual machine within the kernel.

### eBPF Virtual Machine

**eBPF виртуальная машина**

- eBPF VM — это программная модель компьютера, которая исполняет eBPF байткод.
- Байткод нужно преобразовать в машинные инструкции CPU.
- Ранние реализации использовали интерпретацию в ядре: при каждом запуске ядро разбирало инструкции и исполняло их.
- Сейчас интерпретация почти полностью заменена JIT-компиляцией:
  - Компиляция в машинный код происходит один раз при загрузке программы в ядро.
  - Это быстрее и снижает риск некоторых Spectre-уязвимостей.

**Регистры eBPF**

- Используется 10 рабочих регистров: `R0`–`R9`.
- `R10` — указатель на стек (frame pointer), только для чтения.
- Регистры — виртуальные, реализованы в софте (см. `BPF_REG_0`–`BPF_REG_10` в `include/uapi/linux/bpf.h`).
- Контекст программы (аргумент) помещается в `R1` до начала выполнения.
- Возвращаемое значение функции — в `R0`.
- Перед вызовом функции её аргументы раскладываются в `R1`–`R5`.

**Инструкции eBPF**

- В `linux/bpf.h` структура одной инструкции описана как `struct bpf_insn`:
  - `code` — opcode (тип операции)
  - `dst_reg` / `src_reg` — регистры назначения и источника
  - `off` — смещение (offset)
  - `imm` — immediate-константа
- Одна инструкция занимает 64 бита (8 байт), но для 64-битных значений используется «широкое» кодирование в 16 байт.
- eBPF-программа в ядре — это массив структур `bpf_insn`.
- Перед исполнением байткода его проверяет **верификатор**, чтобы гарантировать безопасность.

**Основные типы операций (opcodes)**
- Загрузка значения в регистр (из константы, памяти или другого регистра).
- Запись значения из регистра в память.
- Арифметика (например, сложение с содержимым регистра).
- Переходы (jump) при выполнении условий.

**Дополнительно**

- Полный список инструкций можно найти в «Unofficial eBPF spec» проекта IOVisor и в документации ядра.
- Архитектура eBPF хорошо описана в *BPF and XDP Reference Guide* (документация Cilium).
- Примеры кода на C с использованием `libbpf` находятся в репозитории `github.com/lizrice/learning-ebpf`, директория `chapter3`.

### Краткий конспект: Загрузка и инспекция eBPF-программы

**Загрузка программы в ядро**

- Используется утилита `bpftool` (нужны права root / `sudo`).
- Пример загрузки и «пиннинга» программы:
  ```bash
  bpftool prog load hello.bpf.o /sys/fs/bpf/hello
  ```
- Путь `/sys/fs/bpf/hello` — pinned-объект; отсутствие вывода команды означает успех.
- Проверка:
  ```bash
  ls /sys/fs/bpf
  hello
  ```

**Просмотр загруженных программ**

- Список программ:
  ```bash
  bpftool prog list
  ```
- В выводе видно, например:
  - `id`: уникальный ID программы (например, `540`)
  - `type`: тип программы (`xdp` — можно вешать на сетевой интерфейс)
  - `name`: имя функции из исходника (`hello`)
  - `tag`: хэш инструкций программы
  - `gpl_compatible`: лицензия
  - `loaded_at`: время загрузки
  - `uid`: кто загрузил (обычно `0` — root)
  - `bytes_xlated`: размер eBPF-байткода после верификатора
  - `jited`, `bytes_jited`: включён JIT и размер машинного кода
  - `bytes_memlock`: объём заблокированной (невыгружаемой) памяти
  - `map_ids`: ID BPF-карт, которые использует программа
  - `btf_id`: наличие BTF-метаданных

**Идентификаторы программы**

- `id` — меняется при каждой загрузке/выгрузке.
- `tag` — SHA-сумма инструкций, стабилен при одинаковом коде.
- Обращаться к программе в `bpftool` можно по:
  - `id`
  - `name`
  - `tag`
  - pinned-пути (`/sys/fs/bpf/hello`)
- Имя и tag могут совпадать у нескольких программ, `id` и pinned-путь — уникальны.

**Переведённый (translated) байткод**

- `bytes_xlated` — размер eBPF-кода после проверки верфикатором (код мог быть слегка модифицирован ядром).
- Просмотр переведённого байткода:
  ```bash
  bpftool prog dump xlated name hello
  ```
- Вывод — дизассемблированный eBPF-код с адресами инструкций и операциями над регистрами и картами.
- Он похож на результат `llvm-objdump`, но отражает уже проверенный и, при необходимости, изменённый ядром вариант программы.

### Присоединение eBPF-программы к событию

**Соответствие типа программы и события**

- Тип eBPF-программы должен соответствовать типу события, к которому она крепится (например, `xdp`, `tc`, `flow_dissector` и т.д.).
- В примере используется XDP-программа.

**Присоединение к сетевому интерфейсу**

- Пример с `bpftool`, привязка по ID к XDP-событию на интерфейсе `eth0`:
  ```bash
  bpftool net attach xdp id 540 dev eth0
  ```
- Вместо `id` можно указать:
  - `name` (если уникально),
  - `tag`,
  - либо pinned-путь.

**Просмотр сетевых eBPF-программ**

- Список программ, прикреплённых к сетевым событиям:
  ```bash
  bpftool net list
  ```
- В примере:
  - `xdp: eth0(2) driver id 540` — программа с ID `540` прикреплена к XDP на `eth0`.
  - Показаны и другие возможные точки крепления: `tc`, `flow_dissector`.

**Проверка через `ip link`**

- Пример вывода:
  ```text
  2: eth0: <...> mtu 1500 xdp qdisc fq_codel state UP ...
      prog/xdp id 540 tag 9d0e949f89f1a82c jited
  ```
- Видно, что:
  - у `eth0` есть XDP-программа,
  - она JIT-собрана,
  - `id = 540`, `tag = 9d0e949f89f1a82c`.

- `ip link` также может использоваться для прикрепления/открепления XDP-программ.

**Просмотр trace-логов от программы**

- После прикрепления `hello`-программа печатает сообщения при каждом получении пакета:
  ```bash
  cat /sys/kernel/debug/tracing/trace_pipe
  ```
  или
  ```bash
  bpftool prog tracelog
  ```
- Пример строк:
  ```text
  <idle>-0 [003] ...: bpf_trace_printk: Hello World 4531
  ```
  - `<idle>-0` — нет связанного пользовательского процесса.
  - Событие XDP возникает просто при приходе сетевого пакета, до какой-либо обработки в user space.

**Поведение счётчика**

- В логе видно, что значение счётчика (`counter`) увеличивается на 1 при каждом пакете.
- В исходнике `counter` — глобальная переменная.
- В eBPF глобальные данные реализуются через **BPF map** (далее по тексту главы).

### Глобальные переменные в eBPF

**Карты как глобальные переменные**

- eBPF map — структура данных, доступная как из eBPF-программы, так и из user space.
- Одна и та же карта переиспользуется между запусками программы → можно хранить состояние между вызовами.
- Несколько программ могут использовать одну карту.
- Благодаря этому семантика map используется для реализации **глобальных переменных** и **статических данных**.

**Просмотр карт для примера "Hello World"**

- `bpftool map list` показывает карты с ID, типом и параметрами, напр.:
  - `165: array name hello.bss`
    - `key 4B value 4B max_entries 1`
  - `166: array name hello.rodata`
    - `key 4B value 15B max_entries 1 frozen`
- Имена `.bss` и `.rodata` соответствуют классическим секциям объектного файла из C:
  - `.bss` — глобальные переменные.
  - `.rodata` — константные (read-only) данные.

**hello.bss: глобальная переменная `counter`**

- Содержимое секции/карты:
  ```bash
  bpftool map dump name hello.bss
  ```
  Пример с BTF:
  ```json
  [{
    "value": {
      ".bss": [{
        "counter": 11127
      }]
    }
  }]
  ```
- При повторном вызове видно увеличение `counter`, так как программа выполняется при каждом пакете.

**Роль BTF (debug-инфо)**

- Читаемые имена полей (например, `counter`) `bpftool` показывает **только при наличии BTF**, которая попадает в объект при компиляции с флагом `-g`.
- Без `-g` вывод более «сырой»:
  ```bash
  bpftool map dump name hello.bss
  key: 00 00 00 00 value: 19 01 00 00
  Found 1 element
  ```
- Можно лишь догадаться, что единственное значение — это текущее значение `counter` (в данном примере 0x00000119 = 281).

**hello.rodata: статическая строка**

- Вторая карта (`hello.rodata`) хранит статические данные, например строку для `bpf_printk`:
  ```bash
  bpftool map dump name hello.rodata
  ```
  С BTF:
  ```json
  [{
    "value": {
      ".rodata": [{
        "hello.____fmt": "Hello World %d"
      }]
    }
  }]
  ```
- Без `-g`:
  ```bash
  bpftool map dump id 166
  key: 00 00 00 00 value: 48 65 6c 6c 6f 20 57 6f 72 6c 64 20 25 64 00
  Found 1 element
  ```
  Эти байты — ASCII-строка `"Hello World %d\0"`.

**Итог**

- Глобальные переменные (`counter`) и неизменяемые данные (`"Hello World %d"`) в eBPF реализованы через BPF maps:
  - `.bss` → изменяемое глобальное состояние.
  - `.rodata` → константы.
- Наличие BTF делает вывод `bpftool` человекочитаемым; без него остаются только «сырые» ключи и значения.

### Краткий конспект: Detaching / Unloading eBPF-программы и итог главы

#### Отсоединение программы от события

- Отцепить XDP-программу от сетевого интерфейса:
  ```bash
  bpftool net detach xdp dev eth0
  ```
- При успехе команда не выводит ничего.
- Проверка, что программа больше не прикреплена:
  ```bash
  bpftool net list
  ```
  Пример:
  ```text
  xdp:
  tc:
  flow_dissector:
  ```
  — XDP-записей нет → ни одна программа не привязана.

- Однако сама программа всё ещё **загружена в ядро**:
  ```bash
  bpftool prog show name hello
  ```
  Показывает её ID, tag, xlated/jited размер, `map_ids` и т.д.

#### Выгрузка программы из ядра

- Прямой команды «обратной» `bpftool prog load` нет.
- Программа удаляется, если удалить её pinned-файл:
  ```bash
  rm /sys/fs/bpf/hello
  ```
- После этого:
  ```bash
  bpftool prog show name hello
  ```
  — не даёт вывода: программа полностью выгружена из ядра.

---

### Итоги главы

- Рассмотрен путь: C-код → eBPF-байткод → машинный код (JIT) в ядре.
- Показано, как с помощью `bpftool`:
  - загружать программы (`prog load`) и пиннить их в `sys/fs/bpf`,
  - смотреть список программ (`prog list` / `prog show`),
  - смотреть карты (`map list`, `map dump`),
  - прикреплять к XDP-событиям (`net attach xdp`),
  - отсоединять (`net detach xdp`),
  - выгружать через удаление pinned-файла.
- Примеры разных типов eBPF-программ:
  - XDP — триггер при приходе сетевого пакета на интерфейс;
  - kprobe, tracepoint — триггер при достижении точки в коде ядра.
- Показано, как **maps используются для реализации глобальных переменных** и хранения статических данных:
  - `.bss` → изменяемые глобальные переменные (например, `counter`);
  - `.rodata` → строки/константы.
- Упомянуты вызовы BPF→BPF (функции внутри eBPF-кода).
- Следующая глава разбирает, какие системные вызовы происходят при загрузке/прикреплении программ и карт из user space (через `bpftool` или другое приложение).

