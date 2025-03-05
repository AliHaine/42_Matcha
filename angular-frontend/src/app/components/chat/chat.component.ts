import {Component, inject} from '@angular/core';
import {ChatcardComponent} from "./chatcard/chatcard.component";
import {ChatService} from "../../services/chat.service";
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-chat',
  imports: [
    ChatcardComponent,
    NgForOf
  ],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css'
})
export class ChatComponent {
  chatService = inject(ChatService);

}
