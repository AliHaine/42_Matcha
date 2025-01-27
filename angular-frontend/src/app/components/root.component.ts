import { Component } from '@angular/core';
import {RouterOutlet} from "@angular/router";
import {FooterComponent} from "./footer/footer.component";
import {NavbarComponent} from "./navbar/navbar.component";

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    FooterComponent,
    NavbarComponent
  ],
  template: `<div id="root-content">
              <app-navbar></app-navbar>
              <router-outlet></router-outlet>
              <div id="footer-content">
                 <app-footer></app-footer>
              </div>
            </div>`,
  styles: ['#root-content { height: 100vh; display: flex; flex-direction: column;} #footer-content { margin-top: auto; }']
})
export class RootComponent {}
