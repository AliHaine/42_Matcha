import {inject, Injectable, signal} from '@angular/core';
import {ApiService} from "./api.service";
import {Router} from "@angular/router";
import {WebsocketService} from "./websocket.service";
import {map, Observable, tap} from "rxjs";
import {ProfileModel} from "../models/profile.model";
import {ProfileFactory} from "./profile.factory";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  isLoggedIn = signal<boolean | undefined>(undefined);
  currentUserProfileModel = signal<ProfileModel>(new ProfileModel({}));
  apiService = inject(ApiService);
  router = inject(Router);
  profileFactory = inject(ProfileFactory)
  websocketService = inject(WebsocketService);

  constructor() {
    const token: string | null = this.apiService.getAccessToken();
    if (token === null)
      this.isLoggedIn.set(false);
  }

  accessTokenCheck(): Observable<boolean> {
      return this.apiService.getData("/auth/verify_token", {}).pipe(
          tap(result => {
          if (result["success"] === false) {
            if (result['code'] === "email_confirm") {
              
            }
            this.logout();
          } else
              this.login();
          }),
          map(result => result["success"])
      );
  }

  login() {
    this.websocketService.socketLoaderTmp();
    this.isLoggedIn.set(true);
    this.apiService.getData('/profiles/me', {}).subscribe(result => {
      this.currentUserProfileModel.set(this.profileFactory.getNewProfile(result['user']));
    });
  }

  logout() {
    this.isLoggedIn.set(false);
    this.apiService.postData("/auth/logout", {}).subscribe(result => {
        this.apiService.removeAccessToken();
        this.websocketService.closeSocket();
        window.location.reload();
    });
    // this.apiService.postData("/auth/logout", {}).subscribe(result => {
    //   window.location.reload();
    // });
  }

  refreshCurrentProfile():void {
    this.apiService.getData('/profiles/me', {}).subscribe(result => {
      this.currentUserProfileModel.set(this.profileFactory.getNewProfile(result['user']));
    });
  }
}
