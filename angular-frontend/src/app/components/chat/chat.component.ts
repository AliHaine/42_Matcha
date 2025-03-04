import { Component } from '@angular/core';
import {ChatcardComponent} from "./chatcard/chatcard.component";

@Component({
  selector: 'app-chat',
    imports: [
        ChatcardComponent
    ],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css'
})
export class ChatComponent {

}
