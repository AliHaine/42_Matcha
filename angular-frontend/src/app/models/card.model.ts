import {Interest} from "./interest.model";

export class Card {
    nameAgeCity: String;
    description: String;
    interests: Interest[];
    profilePicturePath: String;

    constructor(nameAgeCity: String, description: String, interests: Interest[], profilePicturePath: String) {
        this.nameAgeCity = nameAgeCity;
        this.description = description;
        this.interests = interests;
        this.profilePicturePath = profilePicturePath;
    }

    getInterestFromIndex(index: number): Interest {
        return <Interest>this.interests.at(index)
    }
}