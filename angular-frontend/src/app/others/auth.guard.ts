import { CanActivateFn, Router} from '@angular/router';
import {inject} from "@angular/core";
import {AuthService} from "../services/auth.service";

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isLoggedIn() === false) {
    router.navigate(['/auth/login']);
    return false;
  } else if (authService.isLoggedIn() === undefined) {
    return authService.accessTokenCheck();
  }
  return true;
};
