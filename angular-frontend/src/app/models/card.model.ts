export class Card {
    nameAgeCity: String;
    description: String;
    interests: [];
    profilePicturePath: String;

    constructor(nameAgeCity: String, description: String, interests: [], profilePicturePath: String) {
        this.nameAgeCity = nameAgeCity;
        this.description = description;
        this.interests = interests;
        this.profilePicturePath = profilePicturePath;
    }
}