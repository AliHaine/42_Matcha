import {Component, inject} from '@angular/core';
import {RouterOutlet} from "@angular/router";
import {FooterComponent} from "./footer/footer.component";
import {NavbarComponent} from "./navbar/navbar.component";
import {AuthService} from "../services/auth.service";
import {NgIf} from "@angular/common";
import {WebsocketService} from "../services/websocket.service";

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    FooterComponent,
    NavbarComponent,
    NgIf
  ],
  template: `<div id="root-content">
              <app-navbar *ngIf="this.authService.isLogin()"></app-navbar>
              <router-outlet></router-outlet>
              <div id="footer-content">
                 <app-footer></app-footer>
              </div>
            </div>`,
  styles: ['#root-content { height: 100vh; display: flex; flex-direction: column;} #footer-content { margin-top: auto; }']
})
export class RootComponent {
  protected readonly inject = inject;
  authService = inject(AuthService);
}
