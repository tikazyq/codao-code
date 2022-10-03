package main

import "github.com/robfig/cron/v3"

func init() {
	// start
	Cron.Start()
}

// Cron create a new cron.Cron instance
var Cron = cron.New()
