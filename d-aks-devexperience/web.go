package main

import (
   "github.com/go-martini/martini"
   "github.com/google/uuid"
)

func main() {
  m := martini.Classic()

  id := uuid.New()

  m.Get("/", func() string {
    return "Version 1: server id " + id.String()
  })

  m.Run()
}