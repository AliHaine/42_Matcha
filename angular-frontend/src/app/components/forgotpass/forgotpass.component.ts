import { Component, inject } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import { ApiService } from '../../services/api.service';
import {
  AbstractControl,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  ValidationErrors,
  ValidatorFn,
  Validators
} from "@angular/forms";
import { Router } from '@angular/router';

@Component({
  selector: 'app-forgotpass',
  imports: [ReactiveFormsModule],
  templateUrl: './forgotpass.component.html',
  styleUrl: './forgotpass.component.css'
})
export class ForgotpassComponent {
  apiService = inject(ApiService);
  router = inject(Router);
  route = inject(ActivatedRoute);
  errorMsg: string = "";

  formGroupForgot = new FormGroup({
    password: new FormControl('', Validators.required),
    passwordConfirm: new FormControl('', Validators.required)
  }, { validators: passwordValidator })

  submit(event: Event) {
    event.preventDefault();
    const token = this.route.snapshot.paramMap.get("token");
    this.apiService.postData("/auth/reset_password", {token: token, password: this.formGroupForgot.value.password}).subscribe(result => {
      if (result["success"]) {
        this.router.navigate(['/login'])
      } else {
        this.errorMsg = result['error'];
      }
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
