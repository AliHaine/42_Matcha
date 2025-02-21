import {Component, inject} from '@angular/core';
import {ApiService} from "../../services/api.service";
import {AuthService} from "../../services/auth.service";
import {FormControl, FormGroup, ReactiveFormsModule} from "@angular/forms";

@Component({
  selector: 'app-account',
  imports: [
    ReactiveFormsModule
  ],
  templateUrl: './account.component.html',
  styleUrl: './account.component.css'
})
export class AccountComponent {

  apiService = inject(ApiService);
  authService = inject(AuthService);
  formGroup: FormGroup = new FormGroup({
    firstname: new FormControl('sa'),
  })

  constructor() {
    this.apiService.getData("/profiles/me", {}).subscribe(result => {
      //this.formGroup.controls
      console.log(result)
    })
  }

  applyTrigger() {

  }

}
