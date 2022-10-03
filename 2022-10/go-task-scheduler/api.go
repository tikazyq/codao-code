package main

import (
	"github.com/gin-gonic/gin"
	"github.com/robfig/cron/v3"
	"net/http"
	"strconv"
)

func GetJobs(c *gin.Context) {
	// return a list of cron job entries
	var results []map[string]interface{}
	for _, e := range Cron.Entries() {
		results = append(results, map[string]interface{}{
			"id":   e.ID,
			"next": e.Next,
		})
	}
	c.JSON(http.StatusOK, results)
}

func AddJob(c *gin.Context) {
	// post JSON payload
	var payload struct {
		Cron string `json:"cron"`
		Exec string `json:"exec"`
	}
	if err := c.ShouldBindJSON(&payload); err != nil {
		c.AbortWithStatus(http.StatusBadRequest)
		return
	}

	// add cron job
	eid, err := Cron.AddFunc(payload.Cron, func() {
		ExecuteTask(payload.Exec)
	})
	if err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, map[string]interface{}{
			"error": err.Error(),
		})
		return
	}

	c.AbortWithStatusJSON(http.StatusOK, map[string]interface{}{
		"id": eid,
	})
}

func DeleteJob(c *gin.Context) {
	// cron job entry id
	id := c.Param("id")
	eid, err := strconv.Atoi(id)
	if err != nil {
		c.AbortWithStatus(http.StatusBadRequest)
		return
	}

	// remove cron job
	Cron.Remove(cron.EntryID(eid))

	c.AbortWithStatus(http.StatusOK)
}
