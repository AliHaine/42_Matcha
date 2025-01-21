import {InterestModel} from "./interest.model";

export class CardModel {
    nameAgeCity: String;
    description: String;
    interests: InterestModel[];
    profilePicturePath: String;

    constructor(nameAgeCity: String, description: String, interests: InterestModel[], profilePicturePath: String) {
        this.nameAgeCity = nameAgeCity;
        this.description = description;
        this.interests = interests;
        this.profilePicturePath = profilePicturePath;
    }

    getInterestFromIndex(index: number): InterestModel {
        return <InterestModel>this.interests.at(index)
    }
}