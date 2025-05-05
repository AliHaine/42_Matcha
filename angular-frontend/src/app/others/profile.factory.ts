import {inject, Injectable} from "@angular/core";
import {ApiService} from "../services/api.service";
import {ProfileModel} from "../models/profile.model";
import {concatMap, from} from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class ProfileFactory {
    apiService = inject(ApiService);

    getNewProfile(data: any): ProfileModel {
        const profile = new ProfileModel(data);
        if (profile.picturesNumber === 0)
            return profile;
        profile.profilePicturePath.set([]);
        const array = Array.from({length: profile.picturesNumber}, (_, i) => i);
        from(array).pipe(
            concatMap(value => this.apiService.getDataImg("/profiles/profile_pictures", {"user_id": profile.userId, "photo_number": value}))
        ).subscribe(result => {
            if (!result)
                return;
            const reader = new FileReader();
            reader.readAsDataURL(result);
            reader.onloadend = () => {
                profile.profilePicturePath.update(arr => [...arr, reader.result as string])
            }
        });
        return profile;
    }
}
