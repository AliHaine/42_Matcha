import {Component, inject, signal} from '@angular/core';
import {RouterLink} from "@angular/router";
import {NotificationComponent} from "../notification/notification.component";
import {NgIf} from "@angular/common";
import {WebsocketService} from "../../services/websocket.service";
import {NotificationService} from "../../services/notification.service";

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, NotificationComponent, NgIf],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {

  showNotif = signal<boolean>(false);
  websocketService = inject(WebsocketService);
  notificationService = inject(NotificationService);

  notificationHover() {
    this.showNotif.set(true);
    if (this.notificationService.notifications().length > 0)
      this.websocketService.sendMessage({"service": "notification", "action": "clear"});
  }

  notificationUnHover() {
    this.showNotif.set(false);
    this.notificationService.notifications.set([]);
  }
}
