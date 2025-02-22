import {CanActivate, Router} from '@angular/router';
import {inject, Injectable} from "@angular/core";
import {AuthService} from "../services/auth.service";
import {Observable, tap} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class LoginGuard implements CanActivate {
  authService = inject(AuthService);
  router = inject(Router);

  canActivate(): boolean {
    return false;
    /*return this.authService.loginAsObservable().pipe(
        tap(isLoggedIn => {
          if (isLoggedIn) {
            console.log("ENTER", isLoggedIn);
            this.router.navigate(['']); // Redirect to home if logged in
          } else
            console.log("ENTER2", isLoggedIn);
        })
    );*/
  }
}
