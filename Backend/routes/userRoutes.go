package routes

import (
    controller "backend/controllers"

    "github.com/gin-gonic/gin"
    "github.com/gorilla/mux"
)

//UserRoutes function
func UserRoutes(incomingRoutes *gin.Engine) {

    var r = mux.NewRouter()

    incomingRoutes.POST("/users/signup", controller.SignUp())
    incomingRoutes.POST("/users/login", controller.Login())
    incomingRoutes.GET("/users/tabla", controller.tablaUsers())
    r.HandleFunc("/users", GetAllUsersEndPoint).Methods("GET")
}