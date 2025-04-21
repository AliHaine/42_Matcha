import {inject, Injectable} from "@angular/core";
import {ApiService} from "./api.service";
import {ProfileModel} from "../models/profile.model";
import {CardService} from "./card.service";

@Injectable({
    providedIn: 'root'
})

export class ProfileActionService {
    apiService = inject(ApiService);
    cardService = inject(CardService);

    likeProfile(profile: ProfileModel) {
        this.apiService.postData(`/profiles/${profile.userId}`, {action: 'like'}).subscribe(_ => {
            console.log(_)
            this.cardService.switchProfile(this.cardService.getIndexFromProfile(profile));
        })
    }

    blockUser(profile: ProfileModel) {
        this.apiService.postData(`/profiles/${profile.userId}`, {"action": "block"}).subscribe(profile => {
            console.log(profile);
        });
    }
}