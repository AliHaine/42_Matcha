import {Injectable, signal} from '@angular/core';
import {ChatModel} from "../models/chat.model";

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  activeChat = signal<number>(0);
  availableChats = signal<ChatModel[]>([]);
  currentChatMessages = signal<string[]>([]);

  constructor() {
    const data = {
      "firstname": "Leila",
      "age": 19,
      "city": "Mulhouse",
      "status": false,
      "lastMsgTime": '12:49',
      "lastMessage": "Lorem ipsum espe fdafdaf afdaf a ..."
    }

    this.availableChats().push(new ChatModel(data))
    data['status'] = true;
    this.availableChats().push(new ChatModel(data))
    this.availableChats().push(new ChatModel(data))
    this.availableChats().push(new ChatModel(data))
    this.availableChats().push(new ChatModel(data))
    this.availableChats().push(new ChatModel(data))
    this.availableChats().push(new ChatModel(data))
    data['status'] = false;
    this.availableChats().push(new ChatModel(data))
  }

  getChatModelAt(index: number) {
    console.log(this.availableChats().at(index))
    return this.availableChats().at(index);
  }
}
