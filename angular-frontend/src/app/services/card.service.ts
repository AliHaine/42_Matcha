import {inject, Injectable, signal, WritableSignal} from '@angular/core';
import {ApiService} from "./api.service";
import {ProfileModel} from "../models/profile.model";
import {ProfileFactory} from "../others/profile.factory";

@Injectable({
    providedIn: 'root'
})
export class CardService {
    apiService: ApiService = inject(ApiService);
    profileFactory: ProfileFactory = inject(ProfileFactory);
    profiles: WritableSignal<ProfileModel[]> = signal<ProfileModel[]>([]);
    private cache_value: number = 200;
    private trigger_cache: number = 130;
    private isFillRunning: boolean = false;

    constructor() {
        this.fillProfiles(this.cache_value);
    }

    refreshProfile(): void {
        this.removeProfilesModel(8);
        if (this.profiles().length < this.trigger_cache)
            this.fillProfiles(this.cache_value - this.profiles().length);
    }

    addNewProfileModel(newProfileModel: ProfileModel): void {
        this.profiles.set([...this.profiles(), newProfileModel]);
    }

    fillProfiles(numberToGet: number) {
        if (this.isFillRunning)
            return;
        this.isFillRunning = true;
        this.apiService.getData("/matcha", {nb_profiles: numberToGet}).subscribe(result => {
            if (!result['success'])
                return;
            for (const data of result["result"]) {
                if (this.isAlreadyLoaded(data['id']))
                    continue;
                this.addNewProfileModel(this.profileFactory.getNewProfile(data));
            }
            this.isFillRunning = false;
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
        if (this.profiles().length < this.trigger_cache)
            this.fillProfiles(this.cache_value - this.profiles().length);
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