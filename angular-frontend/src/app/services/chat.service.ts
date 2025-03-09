import {inject, Injectable, signal} from '@angular/core';
import {ChatModel} from "../models/chat.model";
import {ApiService} from "./api.service";

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  activeChat = signal<number>(0);
  availableChats = signal<ChatModel[]>([]);
  apiService = inject(ApiService);
  currentChatMessages = signal<string[]>([]);

  constructor() {
    /*const data = {
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
    data['status'] = false;
    this.availableChats().push(new ChatModel(data))*/
  }

  getChatModelAt(index: number) {
    console.log(this.availableChats().at(index))
    return this.availableChats().at(index);
  }

  updateAvailableChats(data: number[]) {
    data.forEach((userId) => {
      this.apiService.getData(`/profiles/${userId}`, {}).subscribe(profile => {
        this.availableChats().push(new ChatModel(profile["user"]))
      })
    })
  }
}
