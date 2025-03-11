import {inject, Injectable, signal} from '@angular/core';
import {ApiService} from "./api.service";
import {ProfileModel} from "../models/profile.model";
import {ProfileFactory} from "./profile.factory";

@Injectable({
  providedIn: 'root'
})
export class CardService {

    apiService = inject(ApiService);
    profileFactory = inject(ProfileFactory);
    private profiles = signal<ProfileModel[]>([]);

    constructor() {
        this.refreshProfile();
      }

      refreshProfile() {
        console.log("call refreshProfile");
        this.profiles.set([]);
          this.apiService.getData("/matcha", {nb_profiles: 8}).subscribe(result => {
              for (const data of result["result"]) {
                  this.profiles().push(this.profileFactory.getNewProfile(data));
              }
          });
      }

      getProfiles(): ProfileModel[] {
        console.log("call getProfiles");
          return this.profiles();
      }
}