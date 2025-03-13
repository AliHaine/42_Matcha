import {inject, Injectable, signal} from '@angular/core';
import {ApiService} from "./api.service";
import {Router} from "@angular/router";
import {WebsocketService} from "./websocket.service";
import {map, Observable, tap} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  isLoggedIn = signal<boolean | undefined>(undefined);
  apiService = inject(ApiService);
  router = inject(Router);
  websocketService = inject(WebsocketService);

  constructor() {
    const token: string | null = this.apiService.getAccessToken();
    if (token === null)
      this.isLoggedIn.set(false);
  }

  accessTokenCheck(): Observable<boolean> {
      return this.apiService.getData("/auth/verify_token", {}).pipe(
          tap(result => {
            if (result["success"] === false)
              this.logout();
            else
              this.login();
          }),
          map(result => result["success"])
      );
  }

  login() {
    this.websocketService.socketLoaderTmp();
    this.isLoggedIn.set(true);
  }

  logout() {
    this.isLoggedIn.set(false);
    this.apiService.removeAccessToken();
    this.websocketService.closeSocket();
    this.router.navigate(['auth/login']);
  }
}
