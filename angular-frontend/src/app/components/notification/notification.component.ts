import {Component, inject} from '@angular/core';
import {NotificationService} from "../../services/notification.service";
import {WebsocketService} from "../../services/websocket.service";

@Component({
  selector: 'app-notification',
  imports: [],
  templateUrl: './notification.component.html',
  styleUrl: './notification.component.css'
})
export class NotificationComponent {
  notificationService = inject(NotificationService);
  websocketService = inject(WebsocketService);

  notificationClearAll() {
    if (this.notificationService.notifications().length > 0) {
      this.websocketService.sendMessage({"service": "notification", "action": "clear"});
      this.notificationService.notifications.set([]);
    }
  }

  notificationClear(notificationId: number) {
    console.log(notificationId)
    this.websocketService.sendMessage({"service": "notification", "action": "clear", 'notif_id': notificationId});
    this.notificationClear(notificationId);
  }
}
