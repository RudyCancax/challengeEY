package main

import (
	"fmt"
	// import package http for go web dev
	"net/http"
	// package for log print
	"log"
	// json library
	"encoding/json"

	// gorila mux, router n dispatcher fo go
	"github.com/gorilla/mux"
	// import all local project package
	."backendnojwt/config" // construct read to read db config with toml
	."backendnojwt/dao"    // data access object
	."backendnojwt/models" // to import all model (include User)

	// bson library
	"gopkg.in/mgo.v2/bson"
)

var config = Config{}
var dao = UsersDAO{}

// method handler for get all user
func GetAllUsersEndPoint(w http.ResponseWriter, r *http.Request) {
	users, err := dao.GetAll()
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithJson(w, http.StatusOK, users)
}

// method handler for get user by id
func GetUserByIdEndPoint(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r) // mux library to get all parameters
	user, err := dao.FindUserById(params["id"])
	if err != nil { // data not found
		respondWithError(w, http.StatusBadRequest, "Invalid User ID")
		return
	}
	respondWithJson(w, http.StatusOK, user)
}

// method handler create new user
func CreateUserEndPoint(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()
	var user User
	if err := json.NewDecoder(r.Body).Decode(&user); err != nil { // not valid data struct
		respondWithError(w, http.StatusBadRequest, "Invalid Request")
		return
	}
	user.ID = bson.NewObjectId()
	if err := dao.Insert(user); err != nil { // insert to db
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithJson(w, http.StatusCreated, user)
}

// method handler for update existing user
func UpdateUserEndPoint(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()
	var user User
	if err := json.NewDecoder(r.Body).Decode(&user); err != nil { // invalid data struct
		respondWithError(w, http.StatusBadRequest, "Invalid Request")
		return
	}
	if err := dao.Update(user); err != nil { // update to db
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}
	respondWithJson(w, http.StatusOK, map[string]string{"result": "success"})
}

// method handler to delete existing user
func DeleteUserEndPoint(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()
	var user User
	if err := json.NewDecoder(r.Body).Decode(&user); err != nil { // invalid data struct
		respondWithError(w, http.StatusBadRequest, "Invalid Request")
		return
	}
	if err := dao.Delete(user); err != nil { // delete user
		respondWithError(w, http.StatusInternalServerError, err.Error())
		return
	}

	respondWithJson(w, http.StatusOK, map[string]string{"result": "success"})
}



// method handler for get user by id
func GetUserByEmailEndPoint(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r) // mux library to get all parameters
	user, err := dao.Login(params["email"])
	if err != nil { // data not found
		respondWithError(w, http.StatusBadRequest, "Invalid User Email")
		return
	}
	respondWithJson(w, http.StatusOK, user)
}



// init the connection
// Parse the configuration file 'config.toml', and establish a connection to DB
func init() {
	config.Read()

	dao.Server = config.Server
	dao.Database = config.Database
	dao.Connect()
}

func main() {
	// router with gorilla mux initiate
	var r = mux.NewRouter()

	r.HandleFunc("/users", GetAllUsersEndPoint).Methods("GET")      // call get method for get all user
	r.HandleFunc("/users/{id}", GetUserByIdEndPoint).Methods("GET") // call get method for get spesific user by its id
	r.HandleFunc("/users", CreateUserEndPoint).Methods("POST")      // call post method to create user
	r.HandleFunc("/users", UpdateUserEndPoint).Methods("PUT")       // call put method to edit the user
	r.HandleFunc("/users", DeleteUserEndPoint).Methods("DELETE")    // call delete method to delete the user
	r.HandleFunc("/login/{email}", GetUserByEmailEndPoint).Methods("POST")      // call post method to login

	port := ":8080" // port for run the app

	fmt.Println("Start listening on port", port) // server up

	// Serve server on a port
	if err := http.ListenAndServe(port, r); err != nil {
		log.Fatal() // print error log
	}

}

// method to print error output for http respon
func respondWithError(w http.ResponseWriter, code int, msg string) {
	respondWithJson(w, code, map[string]string{"error": msg})
}

// method to print output for http respon
// parameter  [w (Http.RestponWriter), http.statuscode, payload/data/msg]
// payload is data credential which will be trans to other part
func respondWithJson(w http.ResponseWriter, code int, payload interface{}) {
	response, _ := json.Marshal(payload)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	w.Write(response)
}
