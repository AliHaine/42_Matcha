import {inject, Injectable, signal} from '@angular/core';
import {NotificationModel} from "../models/notification.model";
import {NotificationFactory} from "../others/notification.factory";

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
    notifications = signal<NotificationModel[]>([]);
    notificationFactory = inject(NotificationFactory);

    addNotification(newNotificationData: { [key: string]: any }): void {
      this.notifications.set([...this.notifications(), this.notificationFactory.getNewNotification(newNotificationData)]);
    }

    removeNotifWithId(notifId: number): void {
      this.notifications.update(notifList => notifList.filter(notif => notif.notifId !== notifId));
    }
}
