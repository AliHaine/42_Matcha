import {Component, inject, input, InputSignal} from '@angular/core';
import {ChatModel} from "../../../models/chat.model";
import {FormControl, ReactiveFormsModule} from "@angular/forms";
import {WebsocketService} from "../../../services/websocket.service";
import {ChatbubbleComponent} from "../chatbubble/chatbubble.component";
import {ChatService} from "../../../services/chat.service";
import {NgForOf} from "@angular/common";
import { ApiService } from '../../../services/api.service';
import { MatIconModule } from '@angular/material/icon';
import {PopupService} from "../../../services/popup.service";

@Component({
  selector: 'app-chatarea',
  imports: [
    ReactiveFormsModule,
    ChatbubbleComponent,
    NgForOf,
    MatIconModule,
  ],
  templateUrl: './chatarea.component.html',
  styleUrl: './chatarea.component.css'
})
export class ChatareaComponent {
  webSocketService = inject(WebsocketService);
  chatService = inject(ChatService);
  apiService = inject(ApiService);
  popupService = inject(PopupService);
  chatModel: InputSignal<ChatModel> = input.required();
  messageInput = new FormControl('');

  sendMessage(event: Event) {
    event.preventDefault();

    const pictureAsHtml = document.getElementById('picture') as HTMLInputElement;
    let file: File | undefined;

    file = pictureAsHtml.files?.[0];
    if (file) {
      this.sendImage(file);
      pictureAsHtml.value = '';
    }

    this.webSocketService.sendMessage({"receiver": this.chatModel().userId, "message": this.messageInput.value, "service": "message"});
    this.messageInput.setValue('');
  }

  sendImage(file: File) {
    const formaData = new FormData();

    formaData.append("file", file);
    formaData.append("receiver_id", this.chatModel().userId.toString());
    this.apiService.putData("/chat/upload_file", formaData).subscribe(result => {
      if (!result['success'])
        this.popupService.displayPopupBool(result["message"], result["success"]);
    });
  }
}
