import {Component, inject} from '@angular/core';
import {ApiService} from "../../services/api.service";
import {AuthService} from "../../services/auth.service";

@Component({
  selector: 'app-account',
  imports: [],
  templateUrl: './account.component.html',
  styleUrl: './account.component.css'
})
export class AccountComponent {

  apiService = inject(ApiService);
  authService = inject(AuthService);

}
