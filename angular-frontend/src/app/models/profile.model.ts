export class ProfileModel {
    firstname: string;
    lastname: string;
    age: number;
    city: string;
    gender: string;
    description: string;
    lookingFor: [];
    shape: [];
    health: [];
    picturesNumber: number;
    profilePicturePath: string[] = [];
    status: string;
    userId: number;

    constructor(data: {[key: string]: any}) {
        this.firstname = data["firstname"];
        this.lastname = data["lastname"];
        this.age = data["age"];
        this.city = data["city"];
        this.gender = data["gender"];
        this.description = data["description"];
        this.lookingFor = data["lookingFor"];
        this.shape = data["shape"];
        this.health = data["health"];
        this.picturesNumber = data["picturesNumber"];
        this.profilePicturePath.push("defaultpp.jpg");
        this.status = data["status"];
        this.userId = data["id"];
    }
}