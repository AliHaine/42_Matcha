import {Component, inject, input, InputSignal} from '@angular/core';
import {ChatBubbleModel} from "../../../models/chatbubble.model";
import {NgClass} from "@angular/common";
import {ChatModel} from "../../../models/chat.model";
import {AuthService} from "../../../services/auth.service";

@Component({
  selector: 'app-chatbubble',
  imports: [
    NgClass
  ],
  templateUrl: './chatbubble.component.html',
  styleUrl: './chatbubble.component.css'
})
export class ChatbubbleComponent {
  chatBubble: InputSignal<ChatBubbleModel> = input.required();
  chatModel: InputSignal<ChatModel> = input.required();
  authService = inject(AuthService);

  isSelfBubble(): boolean {
    return this.chatBubble().author_id === this.chatModel().userId;
  }
}
