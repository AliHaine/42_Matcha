import {Component, inject} from '@angular/core';
import {RouterLink} from "@angular/router";
import {ApiService} from "../../../services/api.service";
import {EmailValidator, FormControl, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";

@Component({
  selector: 'app-login',
  imports: [RouterLink, ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

  apiService = inject(ApiService);
  formControlGroup = new FormGroup({
    email: new FormControl('', Validators.required),
    password: new FormControl('', Validators.required),
    checkbox: new FormControl(false)
  });

  submit(event: Event) {
    event.preventDefault();
    console.log(this.formControlGroup.value)
    this.apiService.postData(this.formControlGroup.value);
  }
}
