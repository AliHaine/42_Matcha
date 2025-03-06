import {Component, inject} from '@angular/core';
import {ChatcardComponent} from "./chatcard/chatcard.component";
import {ChatService} from "../../services/chat.service";
import {NgForOf} from "@angular/common";
import {ChatareaComponent} from "./chatarea/chatarea.component";

@Component({
  selector: 'app-chat',
  imports: [
    ChatcardComponent,
    NgForOf,
    ChatareaComponent
  ],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css'
})
export class ChatComponent {
  chatService = inject(ChatService);
}
