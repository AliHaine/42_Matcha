import {InterestModel} from "./interest.model";

export class CardModel {
    firstname: string;
    age: number;
    city: string;
    description: string;
    interests: InterestModel[];
    profilePicturePath: string;
    userId: number;

    constructor(data: { [key: string]: any }) {
        this.firstname = data['firstname'];
        this.age = data['age'];
        this.city = data['city'];
        this.description = data['description'];
        this.interests = [
            new InterestModel("/icons/interest.png", "Interest", data['interests']),
            new InterestModel("/icons/pharmacie.png", "Health", data['health']),
            new InterestModel("/icons/body.png", "Shape", data['shape']),
            new InterestModel("/icons/search.png", "Looking for", data['lookingFor']),
        ];
        this.profilePicturePath = data['picturesNumber'] === 0 ? "defaultpp.jpg" : "defaultpp.jpg";
        this.userId = data['id'];
    }

    getInterestFromIndex(index: number): InterestModel {
        return <InterestModel>this.interests.at(index)
    }

    formateInterest(data: any) {

    }
}