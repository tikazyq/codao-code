package core

import (
	"context"
)

type NodeServiceGrpcServer struct {
	UnimplementedNodeServiceServer

	// channel to receive command
	CmdChannel chan string
}

func (n NodeServiceGrpcServer) ReportStatus(ctx context.Context, request *Request) (*Response, error) {
	return &Response{Data: "ok"}, nil
}

func (n NodeServiceGrpcServer) AssignTask(request *Request, server NodeService_AssignTaskServer) error {
	for {
		select {
		case cmd := <-n.CmdChannel:
			// receive command and send to worker node (client)
			if err := server.Send(&Response{Data: cmd}); err != nil {
				return err
			}
		}
	}
}

var server *NodeServiceGrpcServer

// GetNodeServiceGrpcServer singleton service
func GetNodeServiceGrpcServer() *NodeServiceGrpcServer {
	if server == nil {
		server = &NodeServiceGrpcServer{
			CmdChannel: make(chan string),
		}
	}
	return server
}
