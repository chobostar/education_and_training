package main

import (
	"fmt"
	"sort"
	"strings"
	"sync"
)

// сюда писать код

const (
	multiHashCount = 6
)

func ExecutePipeline(jobs ...job) {
	wg := &sync.WaitGroup{}
	var prevOut chan interface{} = nil
	for _, th := range jobs {
		out := make(chan interface{}, 1)
		wg.Add(1)
		go func(wg *sync.WaitGroup, prevOut, out chan interface{}, th job) {
			defer wg.Done()
			th(prevOut, out)
			close(out)
		}(wg, prevOut, out, th)
		prevOut = out
	}
	wg.Wait()
}

func SingleHash(in, out chan interface{}) {
	quota := make(chan bool, 1)
	wgParent := &sync.WaitGroup{}
	for dataRaw := range in {
		wgParent.Add(1)
		go func(dataRaw interface{}) {
			defer wgParent.Done()
			data := fmt.Sprintf("%v", dataRaw)

			var partOne, partTwo string
			wg := &sync.WaitGroup{}
			wg.Add(2)

			go func(wg *sync.WaitGroup, data string) {
				defer wg.Done()
				partOne = DataSignerCrc32(data)
			}(wg, data)

			go func(wg *sync.WaitGroup, data string, quota chan bool) {
				defer wg.Done()
				quota <- true
				md5 := DataSignerMd5(data)
				<-quota
				partTwo = DataSignerCrc32(md5)
			}(wg, data, quota)

			wg.Wait()

			out <- fmt.Sprintf("%s~%s", partOne, partTwo)
		}(dataRaw)
	}
	wgParent.Wait()
}

func MultiHash(in, out chan interface{}) {
	wgParent := &sync.WaitGroup{}
	for dataRaw := range in {
		wgParent.Add(1)
		go func(dataRaw interface{}) {
			defer wgParent.Done()
			data := fmt.Sprintf("%v", dataRaw)

			wg := &sync.WaitGroup{}
			mu := &sync.Mutex{}
			results := make([]string, multiHashCount)

			for i := 0; i < multiHashCount; i++ {
				wg.Add(1)
				go func(wg *sync.WaitGroup, mu *sync.Mutex, results []string, i int) {
					defer wg.Done()
					result := DataSignerCrc32(fmt.Sprintf("%d%s", i, data))
					mu.Lock()
					results[i] = result
					mu.Unlock()
				}(wg, mu, results, i)
			}

			wg.Wait()
			out <- strings.Join(results, "")
		}(dataRaw)
	}
	wgParent.Wait()
}

func CombineResults(in, out chan interface{}) {
	parts := make([]string, 0)
	for dataRaw := range in {
		data := fmt.Sprintf("%v", dataRaw)

		parts = append(parts, data)
	}
	sort.Strings(parts)
	out <- strings.Join(parts, "_")
}
