import {Component, inject} from '@angular/core';
import {RouterOutlet} from "@angular/router";
import {FooterComponent} from "./footer/footer.component";
import {NavbarComponent} from "./navbar/navbar.component";
import {AuthService} from "../services/auth.service";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    FooterComponent,
    NavbarComponent,
    NgIf
  ],
  template: `<div id="root-content">
              <app-navbar *ngIf="this.authService.isLoggedIn()"></app-navbar>
              <div style="display: flex; align-items: center; justify-content: center; height: 100%; width: 100%">
                <router-outlet></router-outlet>
              </div>
              <app-footer></app-footer>
            </div>`,
  styles: ['#root-content { width: 100vw; height: 100vh; display: flex; flex-direction: column;}']
})
export class RootComponent {
  authService = inject(AuthService);
}
