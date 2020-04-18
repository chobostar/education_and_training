package main

import (
	"bytes"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"path"
	"strconv"
)

func main() {
	out := os.Stdout
	if !(len(os.Args) == 2 || len(os.Args) == 3) {
		panic("usage go run main.go . [-f]")
	}
	path := os.Args[1]
	printFiles := len(os.Args) == 3 && os.Args[2] == "-f"
	err := dirTree(out, path, printFiles)
	if err != nil {
		panic(err.Error())
	}
}

func dirTree(out io.Writer, path string, isPrintFiles bool) error {
	if err := lsDir(out, "", path, isPrintFiles); err != nil {
		return err
	}
	return nil
}

func lsDir(out io.Writer, intend string, p string, isPrintFiles bool) error {
	files, err := readDir(p, isPrintFiles)
	if err != nil {
		return err
	}
	for i, file := range files {
		isLast := i == len(files)-1
		if file.IsDir() {
			printDir(out, intend, file, isLast)
			if err = lsDir(out, intend+getIntend(isLast), path.Join(p, file.Name()), isPrintFiles); err != nil {
				return err
			}
		} else {
			printFile(out, intend, file, isLast)
		}
	}
	return nil
}

func readDir(p string, isPrintFiles bool) ([]os.FileInfo, error) {
	files, err := ioutil.ReadDir(p)
	if err != nil {
		return nil, fmt.Errorf("error while reading dir %v: %v", p, err)
	}
	if isPrintFiles {
		return files, nil
	} else {
		onlyDirs := make([]os.FileInfo, 0)
		for _, file := range files {
			if file.IsDir() {
				onlyDirs = append(onlyDirs, file)
			}
		}
		return onlyDirs, nil
	}
}

func printDir(out io.Writer, intend string, file os.FileInfo, isLast bool) {
	buf := bytes.NewBufferString(intend)
	buf.WriteString(getPrefix(isLast) + file.Name())
	buf.WriteString("\n")
	out.Write(buf.Bytes())
}

func printFile(out io.Writer, intend string, file os.FileInfo, isLast bool) {
	buf := bytes.NewBufferString(intend)
	buf.WriteString(getPrefix(isLast) + file.Name() + " ")

	if size := file.Size(); size == 0 {
		buf.WriteString("(empty)")
	} else {
		buf.WriteString("(" + strconv.FormatInt(size, 10) + "b)")
	}
	buf.WriteString("\n")
	out.Write(buf.Bytes())
}

func getIntend(isLast bool) string {
	if isLast {
		return "\t"
	} else {
		return "│\t"
	}
}

func getPrefix(isLast bool) string {
	if isLast {
		return "└───"
	} else {
		return "├───"
	}
}
