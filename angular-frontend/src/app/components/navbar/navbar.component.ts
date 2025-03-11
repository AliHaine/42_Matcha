import {Component, inject, signal, ChangeDetectionStrategy} from '@angular/core';
import {RouterLink} from "@angular/router";
import {WebsocketService} from "../../services/websocket.service";

@Component({
  selector: 'app-navbar',
  imports: [RouterLink],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
  //changeDetection: ChangeDetectionStrategy.OnPush
})
export class NavbarComponent {

  /*showNotif = signal<boolean>(false);
  websocketService = inject(WebsocketService);*/


  overtest() {
   /* this.showNotif.set(true);
    this.websocketService.sendMessage({"service":"notification","action": "clear"})*/
  }
}
