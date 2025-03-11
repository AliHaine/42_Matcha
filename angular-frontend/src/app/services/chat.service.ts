import {Injectable, signal} from '@angular/core';
import {ChatModel} from "../models/chat.model";

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  availableChats = signal<ChatModel[]>([]);

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
    data['status'] = false;
    this.availableChats().push(new ChatModel(data))
  }

  getChatModelAt(index: number): ChatModel {
    console.log("call getChatModelAt");
    const chatModel: ChatModel = <ChatModel>this.availableChats().at(index);
    /*this.apiService.getData(`/profiles/${chatModel.userId}` , {chat: true, all_messages: true} ).subscribe(data => {
      console.log("data", data);
    });*/
    return chatModel;
  }

  /*updateAvailableChats(data: number[]) {
    this.availableChats.set([]);
    console.log(data);
    from(data).pipe(
        concatMap(userId => this.apiService.getData(`/profiles/${userId}`, {}))
    ).subscribe(result => {
      this.availableChats().push(new ChatModel(result["user"]))
    });*/
    /*data.forEach((userId) => {
      this.apiService.getData(`/profiles/${userId}`, {}).subscribe(profile => {
        this.availableChats().push(new ChatModel(profile["user"]))
      });

      /*this.apiService.getData(`/profiles/${userId}` , {chat: true, all_messages: true} ).subscribe(data => {
        console.log("data", data);
      });*/
    //});
  //}
}
