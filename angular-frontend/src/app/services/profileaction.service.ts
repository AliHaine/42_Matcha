import {inject, Injectable, InputSignal} from "@angular/core";
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
    reportReason: string[] = [];

    constructor() {
        this.apiService.getData("/getInformations/reportReasons", {}).subscribe(result => {
            if (!result)
                return;
            this.reportReason = result["reportReasons"];
        });
    }

    nextProfile(profile: ProfileModel): void {
        this.cardService.switchProfile(this.cardService.getIndexFromProfile(profile));
    }

    likeProfile(profile: ProfileModel): void {
        this.apiService.postData(`/profiles/${profile.userId}`, {action: 'like'}).subscribe(result => {
            if (!result)
                return;
            if (!result['success']) {
                this.popupService.displayPopupBool(result['message'], result['success']);
                return;
            }
            this.cardService.switchProfile(this.cardService.getIndexFromProfile(profile));
            profile.matching.set(result['matching'])
        })
    }

    blockUser(profile: ProfileModel, action: string, reason: string): void {
        this.apiService.postData(`/profiles/${profile.userId}`, {action: action, reason: reason}).subscribe(result => {
            this.popupService.displayPopupBool(result['message'], result['success']);
            if (action === 'block')
                profile.matching.set(result['matching'])
        });
    }
}