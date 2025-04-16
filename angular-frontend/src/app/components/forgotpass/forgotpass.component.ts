import { Component, inject } from '@angular/core';
import { ApiService } from '../../services/api.service';
import {
  AbstractControl, FormArray,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  ValidationErrors,
  ValidatorFn,
  Validators
} from "@angular/forms";

@Component({
  selector: 'app-forgotpass',
  imports: [ReactiveFormsModule],
  templateUrl: './forgotpass.component.html',
  styleUrl: './forgotpass.component.css'
})
export class ForgotpassComponent {
  apiService = inject(ApiService);

  formGroupForgot = new FormGroup({
    password: new FormControl('', Validators.required),
    passwordConfirm: new FormControl('', Validators.required)
  }, { validators: passwordValidator })

  submit(event: Event) {
    event.preventDefault();

    this.apiService.postData("", {password: this.formGroupForgot.value.password}).subscribe(result => {

    })
  }
}

export const passwordValidator: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
  const password: string = <string>control.get('password')?.value;
  if (password.length < 8 || !/[A-Z]/.test(password) || !/[a-z]/.test(password) || !/[1-9]/.test(password))
      return {"securityError": true};

  if (password !== <string>control.get('passwordConfirm')?.value) {
      return {"confirmationError": true};
  }

  return null;
};
