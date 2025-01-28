import {Component, inject} from '@angular/core';
import {FormControl, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {RouterLink} from "@angular/router";
import {ApiService} from "../../../services/api.service";

@Component({
  selector: 'app-register',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {

    apiService = inject(ApiService);
    formControlGroup = new FormGroup({
        lastname: new FormControl('', Validators.required),
        firstname: new FormControl('', Validators.required),
        email: new FormControl('', Validators.required),
        password: new FormControl('', Validators.required),
        passwordconfirm: new FormControl('', Validators.required),
        age: new FormControl('', Validators.required),
        gender: new FormControl('male', Validators.required)
    });

    submit(event: Event) {
      event.preventDefault();
      console.log(this.formControlGroup.value);
      this.apiService.postData('/account/register', this.formControlGroup.value);
    }
}
