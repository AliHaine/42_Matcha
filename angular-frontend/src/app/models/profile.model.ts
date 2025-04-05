import {InterestModel} from "./interest.model";

export class ProfileModel {
    email: string;
    firstname: string;
    lastname: string;
    age: number;
    city: string;
    gender: string;
    description: string;
    lookingFor: [];
    shape: [];
    health: [];
    interests: []
    interestsModels: InterestModel[];
    picturesNumber: number;
    profilePicturePath: string[] = [];
    status: string;
    userId: number;
    fameRate: number;
    hetero: boolean;
    score: number;

    constructor(data: {[key: string]: any}) {
        this.email = data["email"];
        this.firstname = data["firstname"];
        this.lastname = data["lastname"];
        this.age = data["age"];
        this.city = data["city"];
        this.gender = data["gender"];
        this.description = data["description"];
        this.lookingFor = data["lookingFor"];
        this.shape = data["shape"];
        this.health = data["health"];
        this.interests = data['interests'];
        this.interestsModels = [
            new InterestModel("/icons/interest.png", "Interest", data['interests']),
            new InterestModel("/icons/pharmacie.png", "Health", data['health']),
            new InterestModel("/icons/body.png", "Shape", data['shape']),
            new InterestModel("/icons/search.png", "Looking for", data['lookingFor']),
        ];
        this.picturesNumber = data["picturesNumber"];
        this.profilePicturePath.push("defaultpp.jpg");
        this.status = data["status"];
        this.userId = data["id"];
        this.fameRate = data["fame_rate"];
        this.hetero = data["hetero"];
        this.score = data["score"];
    }

    dumpAsDict(): {[key: string]: any} {
        return Object.fromEntries(Object.entries(this));
    }
}