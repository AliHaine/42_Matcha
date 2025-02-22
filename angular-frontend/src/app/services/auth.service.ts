import {inject, Injectable, signal} from '@angular/core';
import {ApiService} from "./api.service";
import {Router} from "@angular/router";
import {WebsocketService} from "./websocket.service";
import {BehaviorSubject, Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private isLoggedIn$ = new BehaviorSubject<boolean>(false);
  apiService = inject(ApiService);
  router = inject(Router);
  websocketService = inject(WebsocketService);

  constructor() {
    const token: string | null = this.apiService.getAccessToken();
    if (token !== null) {
      this.apiService.getData("/auth/verify_token", {}).subscribe(result => {
        if (result["success"] === true) {
          setTimeout(() =>
              {
                this.login();
              },
              2000);
        }
      })
    }
  }

  isLogin(): boolean {
    return this.isLoggedIn$.value;
  }

  login() {
    this.websocketService.socketLoaderTmp();
    this.isLoggedIn$.next(true);
  }

  logout() {
    this.isLoggedIn$.next(false);
    this.apiService.removeAccessToken();
    this.router.navigate(['auth/login']);
  }

  loginAsObservable(): Observable<boolean> {
    return this.isLoggedIn$.asObservable();
  }
}
