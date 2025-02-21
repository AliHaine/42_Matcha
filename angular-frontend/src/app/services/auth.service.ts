import {inject, Injectable, signal} from '@angular/core';
import {ApiService} from "./api.service";
import {Router} from "@angular/router";
import {WebsocketService} from "./websocket.service";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  loggedIn = signal<boolean>(true);
  apiService = inject(ApiService);
  router = inject(Router);
  websocketService = inject(WebsocketService);

  constructor() {
    const token: string | null = this.apiService.getAccessToken();
    if (token !== null) {
      this.apiService.getData("/auth/verify_token", {}).subscribe(result => {
        if (result["success"] === false)
          this.logout();
      })
    }
  }

  isLogin(): boolean {
    return this.loggedIn();
  }

  login() {
    this.websocketService.socketLoaderTmp();
    this.loggedIn.set(true);
  }

  logout() {
    this.loggedIn.set(false);
    this.apiService.removeAccessToken();
    this.router.navigate(['auth/login']);
  }
}
