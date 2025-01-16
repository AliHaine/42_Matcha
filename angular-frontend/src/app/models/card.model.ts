import {Interest} from "./interest.model";

export class Card {
    nameAgeCity: String;
    description: String;
    interests: {};
    profilePicturePath: String;

    constructor(nameAgeCity: String, description: String, interests: { [key: string]: any }, profilePicturePath: String) {
        this.nameAgeCity = nameAgeCity;
        this.description = description;
        for (let key in interests) {
            interests[key] = new Interest(key, "/icons/interest.png", ["a", "b", "c"])
        }
        this.interests = interests;
        this.profilePicturePath = profilePicturePath;
    }
}