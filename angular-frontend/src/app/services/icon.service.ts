import {Injectable} from "@angular/core";
import {IconModel} from "../models/icon.model";

@Injectable({
    providedIn: 'root'
})
export class IconService {



    availableIcons: {[key: string]: IconModel} = {
        "gift": new IconModel("/icons/gift.png", "/icons/gift.gif", null),
        "hearth": new IconModel("/icons/heart.png", "/icons/heart.gif", null),
    };

    getAvailableIcons(iconName: string): IconModel {
        return this.availableIcons[iconName];
    }

    test() {
        const icon: IconModel = this.availableIcons['gift'];
        if (typeof icon.onClickFunction === 'function')
            icon.onClickFunction();
    }



}