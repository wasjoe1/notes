package main

import (
	"fmt" // print stuff
	"os" // open file
	"io" // io error
)

func main() {
	// read a file => use the directory path
	filePath := "../request.http" // first declaration && assignment => re-assign then use =

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
	// finalString := "" // declare + initialize
	var finalString string // declare only; initialized with a zero val (string's 0 val == "")
	
	for {
		n, err := file.Read(buffer) // reads bytes from the file into the buffer; n is num of bytes
		// length = n means => [0, 1, ... n-1]
		if (n > 0) {
			// still have string
			finalString += string(buffer[:n]) // thus n - 1
		}
	
		if (err == io.EOF) {
			// end of file
			fmt.Println(finalString)
			return
			// break
		}
	
		if (err != nil) {
			// error
		}
	}

	// print the tallyed message for now
	fmt.Println(finalString)
}