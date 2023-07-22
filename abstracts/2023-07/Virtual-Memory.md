# Virtual Memory

### 3 memory problems
- Not enought RAM
  - MIPS gives each program its own 32-bit (64) address space
  - Programs can access any byte in their 32-bit (64)  address space
- Holes in out address space
  - Memory fragmentation
- Programs writing over each other

How do we solve this:
- Key to the problem: "same memory space"
- Can we give each program it's own virt memory space?
- If so, we can:
  - Separately map each **program's memory space** to the **RAM memory** space
  - (and even move it to disk if we run OOM)

Mapping gives us **flexibility** in how we use the physical RAM memory

### What is virtual memory (VM) ?

"Any problem in CS can be solved by adding indirection"

VM takes program address and maps them to RAM addresses

#### Solving the problem #1: not enough memory
- map some of the program's address space to the disk (page-out)
- when we need it, we bring it into memory (page-in)

performance penalty

#### Solving the problem #2: holes in the address space
- how do we use the holes left when programs quit?
- we can map a program's addresses to RAM addresses however we like

#### Solving the problem #3: keeping programs secure
- different programs addresses map to different RAM addresses
- Because each program has to own address space, they cannot access each other's data: security and reliability!

Shared memory.

### How does VM works?
- VM: what the program sees
- Physical memory: the physical RAM in the computer

- Virtual addresess (VA) - what the program uses
- Physical addresess (PA) - what the hardware uses to talk to the RAM

Translation map:
1. program executes a load specifying a virtual address VA
2. computer translates the address to the physical address (PA) in memory
3. (If the physical address(PA) is not in memory, the operating system loads it in from disk)
4. The computer then reads the RAM using the physical address (PA) and returns the data to the program 

### Page tables
- the map from VM to PA is the Page table
- so far we have had one Page Table Entry (PTE) for every Virtual Address

- We need to translate every possible address:
  - our progmras have 32-bit (64) VA spaces
  - that's 2^30 words that need Page Table Entries
- How can we make this more manageable?
  - What if we divided memory up into chunks (pages, 4kB) instead of words?
- the Page Table manages larget chucks (pages) of data:
  - Fewer Page Table Entries needed to cover the whole address space
  - But, less flexibility in how to use the RAM (have to move a page at a time)
- Today:
  - Typically 4kB pages (1024 words per page)
  - Sometimes 2MB pages (524288 words per page)

### Address Translation

Virtual Address space:
- Virtual page number (20 bits)
- Page offset (12 bits)

PA space:
- Physical page number (16 bits)
- Page offset (12 bits)  

why 20 bits and 16 bits - we had example with a **4GB** VA space (2^32), but only **256MB** PA space (2^28). So we needed ferwer bits to address our PA space

### Address Translation Example Walkthrough

- virtual page number translated to the physical page number
- page offset untranslated
- page table keeps mappings for every virtual page -> physical page

0x0000304 - 20 bits: virtual page, 12 bit: page offset

