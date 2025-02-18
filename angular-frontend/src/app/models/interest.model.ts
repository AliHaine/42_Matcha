export class InterestModel {
    categoryIconPath: String;
    categoryName: String
    interests: string[];

    constructor(categoryIconPath: String, categoryName: String, interests: string[]) {
        this.categoryIconPath = categoryIconPath;
        this.categoryName = categoryName;
        this.interests = interests;
    }

}