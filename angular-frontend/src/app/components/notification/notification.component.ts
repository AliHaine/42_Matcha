import {Component, inject} from '@angular/core';
import {NotificationService} from "../../services/notification.service";
import {NgForOf, NgIf} from "@angular/common";

@Component({
  selector: 'app-notification',
  imports: [
    NgForOf,
    NgIf
  ],
  templateUrl: './notification.component.html',
  styleUrl: './notification.component.css'
})
export class NotificationComponent {
  notificationService = inject(NotificationService);
}
