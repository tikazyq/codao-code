package main

import (
	"go-distributed-system/core"
	"os"
)

func main() {
	nodeType := os.Args[1]
	switch nodeType {
	case "master":
		core.GetMasterNode().Start()
	case "worker":
		core.GetWorkerNode().Start()
	default:
		panic("invalid node type")
	}
}
