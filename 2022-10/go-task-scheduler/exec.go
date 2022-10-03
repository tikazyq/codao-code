package main

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
)

func ExecuteTask(execCmd string) {
	// execute command string parts, delimited by space
	execParts := strings.Split(execCmd, " ")

	// executable name
	execName := execParts[0]

	// execute command parameters
	execParams := strings.Join(execParts[1:], " ")

	// execute command instance
	cmd := exec.Command(execName, execParams)

	// run execute command instance
	if err := cmd.Run(); err != nil {
		_, err = fmt.Fprintln(os.Stderr, err)
		fmt.Println(err.Error())
	}
}
