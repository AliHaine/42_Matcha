import {ChangeDetectionStrategy, Component, inject, signal} from '@angular/core';
import {RouterLink} from "@angular/router";
import {NotificationComponent} from "../notification/notification.component";
import {WebsocketService} from "../../services/websocket.service";
import {NotificationService} from "../../services/notification.service";
import {MatMenuModule} from '@angular/material/menu';
import {MatButtonModule} from '@angular/material/button';
@Component({
  selector: 'app-navbar',
  imports: [RouterLink, NotificationComponent, MatButtonModule, MatMenuModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class NavbarComponent {

  showNotif = signal<boolean>(false);
  websocketService = inject(WebsocketService);
  notificationService = inject(NotificationService);
  menuItems = [
    { label: 'HOME', link: '/' },
    { label: 'CHATROOM', link: '/chat' },
    { label: 'SEARCH', link: '/search' }
  ]

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
