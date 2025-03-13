import {Component, inject, input, InputSignal} from '@angular/core';
import {ChatModel} from "../../../models/chat.model";
import {ChatService} from "../../../services/chat.service";

@Component({
  selector: 'app-chatcard',
  imports: [],
  templateUrl: './chatcard.component.html',
  styleUrl: './chatcard.component.css'
})
export class ChatcardComponent {
  chatModel: InputSignal<ChatModel> = input.required();
  chatService = inject(ChatService);

  test() {
    console.log("test")
  }
}
