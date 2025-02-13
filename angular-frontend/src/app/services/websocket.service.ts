import {inject, Injectable} from '@angular/core';
import { io, Socket } from 'socket.io-client';
import {ApiService} from "./api.service";

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {

  private websocket: Socket;
  private apiService = inject(ApiService);

  constructor() {
    console.log('Socket.IO Service Initialized');

    this.websocket = io('ws://10.13.1.10:5000', {
      transports: ['websocket'],
      query: { 'access_token': this.apiService.getAccessToken() },
    });

    this.websocket.on('connect', () => {
      console.log('Socket.IO Connected ✅');
      this.sendMessage({ msg: "salut from angular" }); // Send after connection
    });

    this.websocket.on('message', (msg: any) => {
      console.log('Received from server:', msg);
    });

    this.websocket.on('disconnect', () => {
      console.log('Socket.IO Disconnected ❌');
    });
  }

  sendMessage(data: any) {
    this.websocket.emit('message', data);
  }
}
