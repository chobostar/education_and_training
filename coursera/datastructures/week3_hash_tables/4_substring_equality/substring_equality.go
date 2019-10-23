package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)


var m1 int64 = 7541
var m2 int64 = 4703
var x1 int64 = 2
var x2 int64 = 3
var hash1 []int64
var hash2 []int64

func get_power(x, y, p int64) int64 {
	result := int64(1)
	for i := int64(0); i < y; i++ {
		result = (result * x) % p
	}
	return result
}

func prepare_hash(text string, x int64, p int64) []int64 {
	var h []int64
	for i := 0; i < len(text)+1; i++ {
		h = append(h, 0)
	}
	h[0] = 0
	for i := 1; i < len(text)+1; i++ {
		h[i] = ((x * h[i-1] % p) + int64(int(text[i-1]))) % p
	}
	return h
}

func get_hash_of(hash []int64, a, x, p, l int64) int64 {
	result := (((hash[a+l] - get_power(x, l, p) * hash[a]) % p) + p) % p
	return result
}

func get_solve(a, b, l int64) bool {
	if get_hash_of(hash1, a, x1, m1, l) == get_hash_of(hash1, b, x1, m1, l) {
		if get_hash_of(hash2, a, x2, m2, l) == get_hash_of(hash2, b, x2, m2, l) {
			return true
		}
	}
	return false
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	text := readLine(reader)
	count, _ := strconv.ParseInt(readLine(reader), 10, 64)

	hash1 = prepare_hash(text, x1, m1)
	hash2 = prepare_hash(text, x2, m2)

	for i := 0; i < int(count); i++ {
		inputs := strings.Split(strings.TrimSpace(readLine(reader)), " ")
		a, _ := strconv.ParseInt(inputs[0], 10, 64)
		b, _ := strconv.ParseInt(inputs[1], 10, 64)
		l, _ := strconv.ParseInt(inputs[2], 10, 64)

		if get_solve(a, b, l) {
			fmt.Println("Yes")
		} else {
			fmt.Println("No")
		}
	}

}

func readLine(reader *bufio.Reader) string {
	str, _, err := reader.ReadLine()
	if err == io.EOF {
		return ""
	}

	return strings.TrimRight(string(str), "\r\n")
}

func checkError(err error) {
	if err != nil {
		panic(err)
	}
}

/*
bbbabbabaa
6
9 3 1
8 9 1
6 9 1
9 6 1
9 3 1
9 8 1
 */