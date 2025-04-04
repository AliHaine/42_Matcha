import {Component, inject, input, InputSignal} from '@angular/core';
import {RouterLink} from "@angular/router";
import {ChatModel} from "../../../models/chat.model";
import {FormControl, ReactiveFormsModule} from "@angular/forms";
import {WebsocketService} from "../../../services/websocket.service";
import {ChatbubbleComponent} from "../chatbubble/chatbubble.component";
import {ChatService} from "../../../services/chat.service";
import {NgForOf} from "@angular/common";
import { ApiService } from '../../../services/api.service';

@Component({
  selector: 'app-chatarea',
  imports: [
    RouterLink,
    ReactiveFormsModule,
    ChatbubbleComponent,
    NgForOf,
  ],
  templateUrl: './chatarea.component.html',
  styleUrl: './chatarea.component.css'
})
export class ChatareaComponent {
  webSocketService = inject(WebsocketService);
  chatService = inject(ChatService);
  apiService = inject(ApiService);
  chatModel: InputSignal<ChatModel> = input.required();
  messageInput = new FormControl('');

  sendMessage(event: Event) {
    event.preventDefault();

    const pictureAsHtml = document.getElementById('picture') as HTMLInputElement;
    let file: File | undefined;

    file = pictureAsHtml.files?.[0];
    if (file)
      this.sendImage(file);

    this.webSocketService.sendMessage({"receiver": this.chatModel().userId, "message": this.messageInput.value, "service": "message"});
    this.messageInput.setValue('');
  }

  sendImage(file: File) {
    const formaData = new FormData();

    formaData.append("file", file);
    formaData.append("receiver_id", this.chatModel().userId.toString());
    this.apiService.putData("/chat/upload_file", formaData).subscribe(result => {
      if (!result['success'])
        console.log(result);
    });
  }
}
