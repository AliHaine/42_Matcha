import {inject, Injectable} from '@angular/core';
import {ApiService} from "./api.service";
import {Router} from "@angular/router";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  loggedIn: boolean = false;
  apiService = inject(ApiService);
  router = inject(Router)

  constructor() {
    const token: string | null = this.apiService.getAccessToken();
    if (token === null) {
      this.router.navigate(['/auth/login']);
    } else {
      this.apiService.getData("/auth/verify_token", {}).subscribe(result => {
        if (result["success"] === true) {
          this.login();
          this.router.navigate(['']);
        }
        //console.log(result)
      })
    }

  }

  isLogin(): boolean {
    return this.loggedIn;
  }

  login() {
    this.loggedIn = true;
  }

  logout() {
    this.loggedIn = false;
    this.apiService.removeAccessToken();
    this.router.navigate(['auth/login']);
  }
}
