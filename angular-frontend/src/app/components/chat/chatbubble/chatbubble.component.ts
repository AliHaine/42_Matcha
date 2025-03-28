import {Component, input, InputSignal} from '@angular/core';
import {ChatBubbleModel} from "../../../models/chatbubble.model";
import {NgClass} from "@angular/common";

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
  userId: InputSignal<number> = input.required();

  isSelfBubble(): boolean {
    return this.chatBubble().author_id === this.userId();
  }
}
