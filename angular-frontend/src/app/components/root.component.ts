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
  template: `<app-navbar></app-navbar>
             <router-outlet></router-outlet>
             <app-footer></app-footer>`
})
export class RootComponent {}
