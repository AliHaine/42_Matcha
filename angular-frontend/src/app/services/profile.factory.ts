import {inject, Injectable} from "@angular/core";
import {ApiService} from "./api.service";
import {ProfileModel} from "../models/profile.model";

@Injectable({
    providedIn: 'root'
})
export class ProfileFactory {
    apiService = inject(ApiService);

    getNewProfile(data: any): ProfileModel {
        const profile = new ProfileModel(data);
        if (profile.picturesNumber !== 0) {
            this.apiService.getDataImg("/profiles/profile_pictures", {"user_id": profile.userId, "photo_number": 0}).subscribe(result => {
                console.log(result);

            })
        }
        return profile;
    }
}
