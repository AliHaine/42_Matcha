import {Component, input, InputSignal} from '@angular/core';
import {RouterLink} from "@angular/router";
import {ChatModel} from "../../../models/chat.model";
import {FormControl, ReactiveFormsModule} from "@angular/forms";

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
  chatModel: InputSignal<ChatModel> = input.required();
  messageInput = new FormControl('');

  sendMessage(event: Event) {
    event.preventDefault();
    this.messageInput.setValue('');
  }
}
