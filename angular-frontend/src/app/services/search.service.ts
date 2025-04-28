import {inject, Injectable, signal} from '@angular/core';
import {ProfileModel} from "../models/profile.model";
import {ApiService} from "./api.service";
import {ProfileFactory} from "./profile.factory";

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  apiService = inject(ApiService);
  searchProfiles = signal<ProfileModel[]>([]);
  profileFactory = inject(ProfileFactory);
  maxPages: number = 1;
  profilePerPage: number = 2;

  constructor() {
    this.setProfilePerPage(4);
  }

  setProfilePerPage(per_page: number) {
    this.profilePerPage = per_page;
  }

  getSearchProfiles(data: {[key: string]: any}): ProfileModel[] {
    this.searchProfiles.set([]);
    data["profile_per_page"] = this.profilePerPage;
    this.apiService.getData('/research', data).subscribe(result => {
      for (const data of result["result"])
        this.searchProfiles().push(this.profileFactory.getNewProfile(data));
      this.maxPages = result['max_page'];
    })
    return this.searchProfiles();
  }
}
