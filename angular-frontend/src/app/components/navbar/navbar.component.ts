import {Component, inject} from '@angular/core';
import {RouterLink} from "@angular/router";
import {NotificationComponent} from "../notification/notification.component";
import {NgIf} from "@angular/common";
import {WebsocketService} from "../../services/websocket.service";

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, NotificationComponent, NgIf],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {

  showNotif: boolean = true;
  websocketService = inject(WebsocketService);

  overtest() {
    this.showNotif = true;
    this.websocketService.sendMessage({"service":"notification","action": "clear"})
  }
}
