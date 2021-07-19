package models

import "gopkg.in/mgo.v2/bson"

type User struct {
    ID            bson.ObjectId     `bson:"_id" json:"id"`
    First_name    string            `bson:"first_name" json:"first_name"`
    Last_name     string            `bson:"last_name" json:"last_name"`
    Email         string            `bson:"email" json:"email"`
    Password      string            `bson:"password" json:"password"`
    Gender        string            `bson:"gender" json:"gender"`
    Country       string            `bson:"country" json:"country"`
}