import {InterestModel} from "./interest.model";

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
    interests: InterestModel[];
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
        this.interests = [
            new InterestModel("/icons/interest.png", "Interest", data['interests']),
            new InterestModel("/icons/pharmacie.png", "Health", data['health']),
            new InterestModel("/icons/body.png", "Shape", data['shape']),
            new InterestModel("/icons/search.png", "Looking for", data['lookingFor']),
        ];
        this.picturesNumber = data["picturesNumber"];
        this.profilePicturePath.push("defaultpp.jpg");
        this.status = data["status"];
        this.userId = data["id"];
    }
}