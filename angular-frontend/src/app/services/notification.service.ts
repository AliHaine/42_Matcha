import {Injectable, signal} from '@angular/core';
import {NotificationModel} from "../models/notification.model";

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

    notifications = signal<NotificationModel[]>([]);

    addNotification(newNotification: NotificationModel) {
        this.notifications.set([...this.notifications(), newNotification]);
    }
}
