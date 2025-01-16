export class Interest {
    categoryIconPath: String;
    categoryName: String
    interests: [string, string, string];

    constructor(categoryIconPath: String, categoryName: String, interests: [string, string, string]) {
        this.categoryIconPath = categoryIconPath;
        this.categoryName = categoryName;
        this.interests = interests;
    }

}