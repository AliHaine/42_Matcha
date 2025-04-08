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
              <div style="flex: 1; display: flex; align-items: center; justify-content: center; flex: 1;">
                <router-outlet></router-outlet>
              </div>
              <app-footer></app-footer>
            </div>`,
  styles: ['#root-content { display: flex; flex-direction: column; min-height: 100vh;}']
})
export class RootComponent {
  authService = inject(AuthService);
}
