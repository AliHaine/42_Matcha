import {inject, Injectable, signal} from '@angular/core';
import {NotificationModel} from "../models/notification.model";
import {WebsocketService} from "./websocket.service";

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

    websocketService = inject(WebsocketService);
    notifications = signal<NotificationModel[]>([]);

    addNotification(newNotification: NotificationModel) {
        this.notifications.set([...this.notifications(), newNotification]);
    }

    clearNotifications() {
        if (this.notifications().length > 0)
            this.websocketService.sendMessage({"service":"notification","action": "clear"});
    }
}
