```
go test -cover
```

Построение покрытия:
```
go test -coverprofile=cover.out && go tool cover -html=cover.out -o cover.html
```

----
```
go build -o pprof_1.exe pprof_1.go && ./pprof_1.exe

ab -t 300 -n 1000000000 -c 10 http://127.0.0.1:8080/

curl http://127.0.0.1:8080/debug/pprof/heap -o mem_out.txt
curl http://127.0.0.1:8080/debug/pprof/profile?seconds=5 -o cpu_out.txt

go tool pprof -svg -inuse_space pprof_1.exe mem_out.txt > mem_is.svg
go tool pprof -svg -inuse_objects pprof_1.exe mem_out.txt > mem_oo.svg
go tool pprof -svg -alloc_space pprof_1.exe mem_out.txt > mem_as.svg
go tool pprof -svg -alloc_objects pprof_1.exe mem_out.txt > mem_ao.svg
go tool pprof -svg pprof_1.exe cpu_out.txt > cpu.svg
```

горутины:
```
go build -o pprof_2.exe pprof_2.go && ./pprof_2.exe

ab -n 1000 -c 10 http://127.0.0.1:8080/

curl http://localhost:8080/debug/pprof/goroutine?debug=2 -o goroutines.txt
```