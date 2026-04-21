// this version uses string.Builder
package main

import (
	"fmt" // print stuff
	"os" // open file
	"io" // io error
	"strings" // strings.Builder
)

func main() {
	// read a file => use the directory path
	filePath := "./request.http" // first declaration && assignment => re-assign then use =

	// file = open(filePath) // open file
	file, err := os.Open(filePath)
	if (err != nil) {
		// if there is error => return with error; throw error?
		fmt.Println("Error opening file:", err)
		return // go has no try catch throw => just reeturn
	}

	// close file, defer till function ends => mimics finally block
	defer file.Close()

	buffer := make([]byte, 32 * 1024) // create a 32Kb buffer
	var finalString strings.Builder // string.Builder type
	
	for {
		n, err := file.Read(buffer) // reads bytes from the file into the buffer; n is num of bytes
		// length = n means => [0, 1, ... n-1]
		if (n > 0) {
			// still have string => write direct to the string
			finalString.Write(buffer[:n]) // O(k) where k is length of string being added
		}
	
		if (err == io.EOF) {
			// end of file
			// print the tallyed message for now
			fmt.Println(finalString.String()) // O(n) to "join" the entire string
			return
			// break
		}
	
		if (err != nil) {
			// error
			fmt.Println("errpr reading:", err)
		}
	}
}