import {ChangeDetectionStrategy, Component, inject} from '@angular/core';
import {RouterLink} from "@angular/router";
import {WebsocketService} from "../../services/websocket.service";
import {NotificationService} from "../../services/notification.service";
import {MatMenuModule} from '@angular/material/menu';
import {MatButtonModule} from '@angular/material/button';
import { AuthService } from '../../services/auth.service';
import { MatIconModule } from '@angular/material/icon';
import {SvgIconService} from "../../services/svg-icon.service";

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, MatButtonModule, MatMenuModule, MatIconModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class NavbarComponent {

  websocketService = inject(WebsocketService);
  notificationService = inject(NotificationService);
  svgIconService = inject(SvgIconService);
  authService = inject(AuthService);

  notificationHover() {
    if (this.notificationService.notifications().length > 0)
      this.websocketService.sendMessage({"service": "notification", "action": "clear"});
  }

  notificationUnHover() {
    this.notificationService.notifications.set([]);
  }
}
