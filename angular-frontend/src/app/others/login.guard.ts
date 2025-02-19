import {CanActivateFn, Router} from '@angular/router';
import {inject} from "@angular/core";
import {AuthService} from "../services/auth.service";

export const loginGuard: CanActivateFn = (route, state) => {

  const authService = inject(AuthService);
  const router = inject(Router);

  console.log("enter")
  if (authService.isLogin()) {
    router.navigate(['']);
    return false;
  }

  return true;
};
