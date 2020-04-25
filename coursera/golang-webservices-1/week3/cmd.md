```
go test -bench . -benchmem
go test -bench . -benchmem -cpuprofile=cpu.out -memprofile=mem.out -memprofilerate=1 *.go
go tool pprof main.test cpu.out
go tool pprof main.test mem.out

    top
        list <method-name>
    web
        alloc_objects
        alloc_space
```