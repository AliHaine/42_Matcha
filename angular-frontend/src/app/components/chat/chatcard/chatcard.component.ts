import {Component, input, InputSignal} from '@angular/core';
import {ChatModel} from "../../../models/chat.model";

@Component({
  selector: 'app-chatcard',
  imports: [],
  templateUrl: './chatcard.component.html',
  styleUrl: './chatcard.component.css'
})
export class ChatcardComponent {
  chatModel: InputSignal<ChatModel> = input.required();
}
