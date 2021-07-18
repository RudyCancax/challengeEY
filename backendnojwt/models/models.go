package models

import "gopkg.in/mgo.v2/bson"

// Represents a user, use bson keyword to tell mgo driver
// how to name the properties mongodb document
// type User struct {
// 	ID       bson.ObjectId `bson:"_id" json:"id"`
// 	Name     string        `bson:"name" json:"name"`
// 	Email    string        `bson:"email" json:"email"`
// 	No_hp    string        `bson:"no_hp" json:"no_hp"`
// 	Event_id string        `bson:"event_id" json:"event_id"`
// }


type User struct {
    ID            bson.ObjectId     `bson:"_id" json:"id"`
    First_name    string            `bson:"first_name" json:"first_name"`
    Last_name     string            `bson:"last_name" json:"last_name"`
    Password      string            `bson:"password" json:"password"`
    Email         string            `bson:"email" json:"email"`
}