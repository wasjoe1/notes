// final cleaned version
package main

import (
	"fmt"
	"os"
	"io"
	"strings"
)

func main() {
	filePath := "./request.http"

	file, err := os.Open(filePath)
	if (err != nil) {
		fmt.Println("Error opening file:", err)
		return
	}

	defer file.Close()

	buffer := make([]byte, 32 * 1024)
	var finalString strings.Builder
	
	for {
		n, err := file.Read(buffer)
		if (n > 0) {
			finalString.Write(buffer[:n])
		}
	
		if (err == io.EOF) {
			fmt.Println(finalString.String())
			return
		}
	
		if (err != nil) {
			fmt.Println("error reading:", err)
		}
	}
}