import {Component, input, InputSignal} from '@angular/core';
import {ChatBubbleModel} from "../../../models/chatbubble.model";

@Component({
  selector: 'app-chatbubble',
  imports: [],
  templateUrl: './chatbubble.component.html',
  styleUrl: './chatbubble.component.css'
})
export class ChatbubbleComponent {
  chatBubble: InputSignal<ChatBubbleModel> = input.required();
}
