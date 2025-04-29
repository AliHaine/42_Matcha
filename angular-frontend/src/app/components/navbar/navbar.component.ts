import {ChangeDetectionStrategy, Component, inject} from '@angular/core';
import {RouterLink} from "@angular/router";
import {MatMenuModule} from '@angular/material/menu';
import {MatButtonModule} from '@angular/material/button';
import { AuthService } from '../../services/auth.service';
import { MatIconModule } from '@angular/material/icon';
import {NotificationService} from "../../services/notification.service";

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, MatButtonModule, MatMenuModule, MatIconModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class NavbarComponent {
  authService = inject(AuthService);
  notificationService = inject(NotificationService);
}
