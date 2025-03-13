import {inject, Injectable, signal} from '@angular/core';
import {ChatModel} from "../models/chat.model";
import {ApiService} from "./api.service";
import {concatMap, from} from "rxjs";
import {ChatBubbleModel} from "../models/chatbubble.model";

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  apiService = inject(ApiService);
  activeChat = signal<ChatModel | undefined>(undefined);
  availableChats = signal<ChatModel[]>([]);
  currentChatBubbles = signal<ChatBubbleModel[]>([]);

  updateCurrentChat(chatModel: ChatModel): ChatModel {
    console.log("enter");
    this.activeChat.set(chatModel);
    this.apiService.getData(`/profiles/${chatModel.userId}` , {chat: true, all_messages: true} ).subscribe(data => {
      console.log("data", data);
      this.setupAllBubbles(data["user"]["allMessages"]);
    });
    return chatModel;
  }

  updateAvailableChats(data: number[]) {
    this.availableChats.set([]);
    console.log(data);
    from(data).pipe(
        concatMap(userId => this.apiService.getData(`/profiles/${userId}`, {"chat": true, "all_messages": false}))
    ).subscribe(result => {
      console.log(result)
      this.addNewChatModel(new ChatModel(result["user"]));
    });
  }

  setupAllBubbles(data: []) {
    this.currentChatBubbles.set([]);
    data.forEach(value => {
      this.addNewChatBubbleModel(value);
    });
  }

  addNewChatModel(newChatModel: ChatModel) {
    this.availableChats.set([...this.availableChats(), newChatModel]);
  }

  addNewChatBubbleModel(data: {}) {
    this.currentChatBubbles.set([ new ChatBubbleModel(data), ...this.currentChatBubbles()]);
  }
}
