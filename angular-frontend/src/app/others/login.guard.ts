import { CanActivateFn, Router} from '@angular/router';
import {inject} from "@angular/core";
import {AuthService} from "../services/auth.service";
import {map, tap} from "rxjs";

export const loginGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isLoggedIn === true) {
    router.navigate(['']);
    return false;
  } else if (authService.isLoggedIn === undefined) {
    return authService.tmpTokenCheck().pipe(
        tap(result => {
          if (result)
            router.navigate([''])
        }),
        map(_ => _)
    );
  }
  return true;
}
