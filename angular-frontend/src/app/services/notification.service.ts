import {Injectable, signal} from '@angular/core';
import {NotificationModel} from "../models/notification.model";

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
    notifications = signal<NotificationModel[]>([]);

    addNotification(newNotification: NotificationModel): void {
      this.notifications.set([...this.notifications(), newNotification]);
    }

    removeNotifWithId(notifId: number): void {
      //this.notifications.update(notifList => notifList.filter(notif => notif.notifId !== notifId));
    }
}
