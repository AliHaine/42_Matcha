import { Injectable } from '@angular/core';
import {NotificationModel} from "../models/notification.model";

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

    notifications: NotificationModel[] = [];

    constructor() { }
}
