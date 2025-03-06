import {Component, input, InputSignal} from '@angular/core';
import {RouterLink} from "@angular/router";
import {ChatModel} from "../../../models/chat.model";

@Component({
  selector: 'app-chatarea',
  imports: [
    RouterLink
  ],
  templateUrl: './chatarea.component.html',
  styleUrl: './chatarea.component.css'
})
export class ChatareaComponent {
  chatModel: InputSignal<ChatModel> = input.required();
}
