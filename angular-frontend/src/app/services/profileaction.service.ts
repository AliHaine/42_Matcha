import {inject, Injectable} from "@angular/core";
import {ApiService} from "./api.service";
import {ProfileModel} from "../models/profile.model";
import {CardService} from "./card.service";
import {PopupService} from "./popup.service";

@Injectable({
    providedIn: 'root'
})

export class ProfileActionService {
    apiService = inject(ApiService);
    cardService = inject(CardService);
    popupService = inject(PopupService);

    likeProfile(profile: ProfileModel) {
        this.apiService.postData(`/profiles/${profile.userId}`, {action: 'like'}).subscribe(result => {
            if (!result['success'])
                this.popupService.displayPopupBool(result['message'], result['success'])
            this.cardService.switchProfile(this.cardService.getIndexFromProfile(profile));
        })
    }

    blockUser(profile: ProfileModel, action: string) {
        this.apiService.postData(`/profiles/${profile.userId}`, {action: action}).subscribe(_ => {
        });
    }
}