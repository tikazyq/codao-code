package core

import (
	"github.com/gin-gonic/gin"
	"google.golang.org/grpc"
	"net"
	"net/http"
)

// MasterNode is the node instance
type MasterNode struct {
	api     *gin.Engine            // api server
	ln      net.Listener           // listener
	svr     *grpc.Server           // grpc server
	nodeSvr *NodeServiceGrpcServer // node service
}

func (n *MasterNode) Init() (err error) {
	// grpc server listener with port as 50051
	n.ln, err = net.Listen("tcp", ":50051")
	if err != nil {
		return err
	}

	// grpc server
	n.svr = grpc.NewServer()

	// node service
	n.nodeSvr = GetNodeServiceGrpcServer()

	// register node service to grpc server
	RegisterNodeServiceServer(n.svr, n.nodeSvr)

	// api
	n.api = gin.Default()
	n.api.POST("/tasks", func(c *gin.Context) {
		// parse payload
		var payload struct {
			Cmd string `json:"cmd"`
		}
		if err := c.ShouldBindJSON(&payload); err != nil {
			c.AbortWithStatus(http.StatusBadRequest)
			return
		}

		// send command to node service
		n.nodeSvr.CmdChannel <- payload.Cmd

		c.AbortWithStatus(http.StatusOK)
	})

	return nil
}

func (n *MasterNode) Start() {
	// start grpc server
	go n.svr.Serve(n.ln)

	// start api server
	_ = n.api.Run(":9092")

	// wait for exit
	n.svr.Stop()
}

var masterNode *MasterNode

// GetMasterNode returns the node instance
func GetMasterNode() *MasterNode {
	if masterNode == nil {
		// node
		masterNode = &MasterNode{}

		// initialize node
		if err := masterNode.Init(); err != nil {
			panic(err)
		}
	}

	return masterNode
}
