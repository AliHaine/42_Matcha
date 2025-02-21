import { Component } from '@angular/core';
import {RouterLink} from "@angular/router";
import {NotificationComponent} from "../notification/notification.component";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, NotificationComponent, NgIf],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {

  showNotif: boolean = false;

  overtest() {
    this.showNotif = true;
    console.log("hover")
  }
}
