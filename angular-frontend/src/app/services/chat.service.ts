import {inject, Injectable, signal} from '@angular/core';
import {ChatModel} from "../models/chat.model";
import {ApiService} from "./api.service";
import {concatMap, from, map} from "rxjs";
import {ChatBubbleModel} from "../models/chatbubble.model";
import { BubbleFactory } from './bubble.factory';

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  apiService = inject(ApiService);
  bubbleFactory = inject(BubbleFactory);
  activeChat = signal<ChatModel | undefined>(undefined);
  availableChats = signal<ChatModel[]>([]);
  currentChatBubbles = signal<ChatBubbleModel[]>([]);

  updateCurrentChat(chatModel: ChatModel): ChatModel {
    this.activeChat.set(chatModel);
    this.apiService.getData(`/profiles/${chatModel.userId}` , {chat: true, all_messages: true} ).subscribe(data => {
        console.log(data)
      this.setupAllBubbles(data["user"]["allMessages"]);
    });
    return chatModel;
  }

  updateAvailableChats(data: number[]) {
    this.availableChats.set([]);
    from(data).pipe(
        concatMap(userId =>
            this.apiService.getData(`/profiles/${userId}`, { "chat": true, "all_messages": false }).pipe(
                map(result => result["user"])
            )
        ),
        concatMap(user =>
            this.apiService.getDataImg("/profiles/profile_pictures", { "user_id": user.id, "photo_number": 0 }).pipe(
                map(imageBlob => ({ user, imageBlob }))
            )
        )
    ).subscribe(({ user, imageBlob }) => {
        if (user.picturesNumber === 0) {
          this.addNewChatModel(new ChatModel(user));
          return;
        }
        const reader = new FileReader();
        reader.readAsDataURL(imageBlob);
        reader.onloadend = () => {
            user.picturePath = reader.result as string;
            this.addNewChatModel(new ChatModel(user));
        };
    });
  }

  setupAllBubbles(data: []) {
    this.currentChatBubbles.set([]);
    if (data === undefined ||  data.length === 0)
      return;
    data.forEach(value => {
      this.addNewChatBubbleModel(value);
    });
  }

  addNewChatModel(newChatModel: ChatModel) {
    this.availableChats.set([...this.availableChats(), newChatModel]);
  }

  addNewChatBubbleModel(data: {}) {
    this.currentChatBubbles.set([this.bubbleFactory.getNewBubble(data), ...this.currentChatBubbles()]);
  }
}
