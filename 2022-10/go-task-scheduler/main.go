package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"os"
)

func main() {
	// api engine
	app := gin.New()

	// api routes
	app.GET("/jobs", GetJobs)
	app.POST("/jobs", AddJob)
	app.DELETE("/jobs/:id", DeleteJob)

	// run api
	if err := app.Run(":9092"); err != nil {
		_, err = fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
