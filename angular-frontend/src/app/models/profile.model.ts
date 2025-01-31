export class ProfileModel {

    firstname: String;
    lastname: String;
    age: Number;
    city: String;
    gender: String;
    description: String;
    lookingFor: [];
    shape: [];
    health: [];
    interests: [];
    picturesNumber: Number;
    status: String;

    constructor(firstname: String, lastname: String, age: Number, city: String, gender: String, description: String, lookingFor: [], shape: [], health: [], interests: [], picturesNumber: number, status: String) {
        this.firstname = firstname;
        this.lastname = lastname;
        this.age = age;
        this.city = city;
        this.gender = gender;
        this.description = description;
        this.lookingFor = lookingFor;
        this.shape = shape;
        this.health = health;
        this.interests = interests;
        this.picturesNumber = picturesNumber
        this.status = status;
    }

}