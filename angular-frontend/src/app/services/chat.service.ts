import {Injectable, signal} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  activeChat = signal<number>(0);
  availableChats = signal<number[]>([0,1,2,3,4]);
  currentChatMessages = signal<string[]>([]);

  constructor() { }
}
