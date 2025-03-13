import {Component, inject, input, InputSignal} from '@angular/core';
import {RouterLink} from "@angular/router";
import {ChatModel} from "../../../models/chat.model";
import {FormControl, ReactiveFormsModule} from "@angular/forms";
import {WebsocketService} from "../../../services/websocket.service";
import {ChatbubbleComponent} from "../chatbubble/chatbubble.component";
import {ChatService} from "../../../services/chat.service";
import {NgForOf} from "@angular/common";

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
  chatModel: InputSignal<ChatModel> = input.required();
  messageInput = new FormControl('');

  sendMessage(event: Event) {
    event.preventDefault();
    this.webSocketService.sendMessage({"receiver": this.chatModel().userId, "message": this.messageInput.value, "service": "message"});
    this.messageInput.setValue('');
  }
}
