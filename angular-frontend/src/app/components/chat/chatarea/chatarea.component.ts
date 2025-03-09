import {Component, inject, input, InputSignal} from '@angular/core';
import {RouterLink} from "@angular/router";
import {ChatModel} from "../../../models/chat.model";
import {FormControl, ReactiveFormsModule} from "@angular/forms";
import {WebsocketService} from "../../../services/websocket.service";

@Component({
  selector: 'app-chatarea',
  imports: [
    RouterLink,
    ReactiveFormsModule
  ],
  templateUrl: './chatarea.component.html',
  styleUrl: './chatarea.component.css'
})
export class ChatareaComponent {
  webSocketService = inject(WebsocketService);
  chatModel: InputSignal<ChatModel> = input.required();
  messageInput = new FormControl('');

  sendMessage(event: Event) {
    event.preventDefault();
    this.webSocketService.sendMessage({"receiver": this.chatModel().userId, "message": "salut"})
    this.messageInput.setValue('');
  }
}
