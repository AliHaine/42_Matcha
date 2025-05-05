import {ChangeDetectionStrategy, Component, inject} from '@angular/core';
import {NotificationService} from "../../services/notification.service";
import {WebsocketService} from "../../services/websocket.service";
import {Router, RouterLink} from "@angular/router";
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-notification',
  imports: [
    RouterLink,
    MatIconModule
  ],
  templateUrl: './notification.component.html',
  styleUrl: './notification.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class NotificationComponent {
  notificationService = inject(NotificationService);
  websocketService = inject(WebsocketService);
  router = inject(Router);

  notificationClearAll() {
    if (this.notificationService.notifications().length > 0) {
      this.websocketService.sendMessage({"service": "notification", "action": "clear"});
      this.notificationService.notifications.set([]);
    }
  }

  notificationClear(notificationId: number) {
    this.websocketService.sendMessage({"service": "notification", "action": "clear", 'notif_id': notificationId});
    this.notificationService.removeNotifWithId(notificationId);
  }
}
