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
    username: string;
    premium: boolean;
    matching: string;
    lastConnetion: string;

    constructor(data: {[key: string]: any}) {
        console.log(data)
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
        this.username = data["username"];
        this.premium = data["premium"];
        this.matching = data["matching"]
        this.lastConnetion = data["last_connection"];
    }

    dumpAsDict(): {[key: string]: any} {
        return Object.fromEntries(Object.entries(this));
    }
}