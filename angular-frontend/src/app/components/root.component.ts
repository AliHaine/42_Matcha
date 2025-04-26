import {Component, inject} from '@angular/core';
import {RouterOutlet} from "@angular/router";
import {FooterComponent} from "./footer/footer.component";
import {NavbarComponent} from "./navbar/navbar.component";
import {AuthService} from "../services/auth.service";
import {PopupComponent} from "./utils/popup/popup.component";


@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    FooterComponent,
    NavbarComponent,
    PopupComponent,
  ],
  template:
  `
    <div id="root-content">
      <app-navbar></app-navbar>
      <div style="flex: 1;">
        <router-outlet></router-outlet>
      </div>
      <app-footer></app-footer>
    </div>
    <app-popup/>
  `,
  styles: ['#root-content { display: flex; flex-direction: column; min-height: 100vh;}']
})
export class RootComponent {
  authService = inject(AuthService);
}
