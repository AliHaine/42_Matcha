import {inject, Injectable, signal, WritableSignal} from '@angular/core';
import {ApiService} from "./api.service";
import {ProfileModel} from "../models/profile.model";
import {ProfileFactory} from "./profile.factory";

@Injectable({
    providedIn: 'root'
})
export class CardService {

    apiService: ApiService = inject(ApiService);
    profileFactory: ProfileFactory = inject(ProfileFactory);
    profiles: WritableSignal<ProfileModel[]> = signal<ProfileModel[]>([]);

    constructor() {
        this.fillProfiles(24);
    }

    refreshProfile(numberToGet: number): void {
        this.removeProfilesModel(8);
        if (this.profiles.length < 13)
            numberToGet += 10;
        this.fillProfiles(numberToGet);
    }

    addNewProfileModel(newProfileModel: ProfileModel): void {
        this.profiles.set([...this.profiles(), newProfileModel]);
    }

    fillProfiles(numberToGet: number) {
        this.apiService.getData("/matcha", {nb_profiles: numberToGet}).subscribe(result => {
            for (const data of result["result"]) {
                if (this.isAlreadyLoaded(data['id']))
                    continue;
                this.addNewProfileModel(this.profileFactory.getNewProfile(data));
            }
        });
    }

    removeProfilesModel(numberToRemove: number): void {
        this.profiles.update(profiles => [...profiles.slice(numberToRemove)]);
    }

    removeProfileAtIndex(index: number): void {
        this.profiles.update(profiles => [...profiles.slice(0, index-1), ...profiles.slice(index, profiles.length)]);
    }

    switchProfile(index: number): void {
        this.profiles.update(profiles => {
            const newProfiles = [...profiles];
            newProfiles[index] = newProfiles[8];
            return newProfiles;
        });
        this.removeProfileAtIndex(9);
        if (this.profiles().length < 13)
            this.fillProfiles(20);
    }

    getIndexFromProfile(profile: ProfileModel): number {
        return this.profiles().indexOf(profile);
    }

    isAlreadyLoaded(newId: number) {
        for (const profile of this.profiles()) {
            if (profile.userId == newId)
                return true;
        }
        return false;
    }
}