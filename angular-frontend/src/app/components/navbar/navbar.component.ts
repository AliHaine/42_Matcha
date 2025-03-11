import {Component, inject} from '@angular/core';
import {RouterLink} from "@angular/router";
import {WebsocketService} from "../../services/websocket.service";

@Component({
  selector: 'app-navbar',
  imports: [RouterLink],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {

  showNotif: boolean = false;
  websocketService = inject(WebsocketService);

  overtest() {
    this.showNotif = true;
    this.websocketService.sendMessage({"service":"notification","action": "clear"})
  }
}
