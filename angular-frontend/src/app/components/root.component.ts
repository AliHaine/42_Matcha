import {Component, inject} from '@angular/core';
import {RouterOutlet} from "@angular/router";
import {NavbarComponent} from "./navbar/navbar.component";

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    NavbarComponent,
  ],
  template: `<div id="root-content">
              <app-navbar></app-navbar>
              <router-outlet></router-outlet>
            </div>`,
  styles: ['#root-content { height: 100vh; display: flex; flex-direction: column;} #footer-content { margin-top: auto; }']
})
export class RootComponent {
}
