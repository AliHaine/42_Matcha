export class InterestModel {
    categoryIconPath: string;
    categoryName: string
    interests: string[];

    constructor(categoryIconPath: string, categoryName: string, interests: string[]) {
        this.categoryIconPath = categoryIconPath;
        this.categoryName = categoryName;
        this.interests = interests;
    }

}