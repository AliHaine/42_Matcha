import {inject, Injectable, NgZone} from '@angular/core';
import { io, Socket } from 'socket.io-client';
import {ApiService} from "./api.service";
import {NotificationService} from "./notification.service";
import {NotificationModel} from "../models/notification.model";
import {backendIP} from "../app.config";
import {ChatService} from "./chat.service";

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {

  private websocket: Socket | undefined;
  private apiService = inject(ApiService);
  private chatService = inject(ChatService);
  private notificationService = inject(NotificationService);
  private ngZone = inject(NgZone);

  constructor() {
  }

  socketLoaderTmp() {
    console.log('Socket.IO Service Initialized');

    this.ngZone.runOutsideAngular(() => {
      this.websocket = io(`ws://${backendIP}:5000`, {
        transports: ['websocket'],
        query: { 'access_token': this.apiService.getAccessToken() },
      });

      this.websocket.on('connect', () => {
        console.log('Socket.IO Connected ✅');
        this.sendMessage({ msg: "salut from angular" }); // Send after connection
      });

      this.websocket.on('notification', (msg: any) => {
        console.log("notification")
        this.notificationService.notifications.push(new NotificationModel(msg.author_id, msg.author_name, msg.action))
      });

      this.websocket.on('message', (msg: any) => {
        console.log(msg)
      });

      this.websocket.on('available_chats', (msg: any) => {
        this.chatService.updateAvailableChats(msg["users"]);
      });

      this.websocket.on('disconnect', () => {
        console.log('Socket.IO Disconnected ❌');
      });
    });
  }

  closeSocket() {
    this.websocket?.disconnect();
  }

  sendMessage(data: any) {
    if (this.websocket !== undefined)
      this.websocket.emit('message', data);
  }
}
