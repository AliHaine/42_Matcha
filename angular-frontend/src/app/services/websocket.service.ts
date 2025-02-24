import {inject, Injectable} from '@angular/core';
import { io, Socket } from 'socket.io-client';
import {ApiService} from "./api.service";
import {NotificationService} from "./notification.service";
import {NotificationModel} from "../models/notification.model";

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {

  private websocket: Socket | undefined;
  private apiService = inject(ApiService);
  private notificationService = inject(NotificationService);

  constructor() {
  }

  socketLoaderTmp() {
    console.log('Socket.IO Service Initialized');

    this.websocket = io('ws://127.0.0.1:5000', {
      transports: ['websocket'],
      query: { 'access_token': this.apiService.getAccessToken() },
    });

    this.websocket.on('connect', () => {
      console.log('Socket.IO Connected ✅');
      this.sendMessage({ msg: "salut from angular" }); // Send after connection
    });

    this.websocket.on('notification', (msg: any) => {
      console.log(msg)
      this.notificationService.notifications.push(new NotificationModel(msg.author_id, msg.author_name, msg.action))
    });

    this.websocket.on('available_chats', (msg: any) => {
      console.log(msg)
    });

    this.websocket.on('disconnect', () => {
      console.log('Socket.IO Disconnected ❌');
    });
  }

  sendMessage(data: any) {
    if (this.websocket !== undefined)
      this.websocket.emit('message', data);
  }
}
