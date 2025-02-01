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

    constructor(data: {}) {
        this.firstname = data["firstname"];
        this.lastname = data["lastname"];
        this.age = data["age"];
        this.city = data["city"];
        this.gender = data["gender"];
        this.description = data["description"];
        this.lookingFor = data["lookingFor"];
        this.shape = data["shape"];
        this.health = data["health"];
        this.interests = data["interests"];
        this.picturesNumber = data["picturesNumber"];
        this.status = data["status"];
    }

}