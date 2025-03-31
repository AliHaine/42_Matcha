import {Component, inject} from '@angular/core';
import {Router, RouterLink} from "@angular/router";
import {ApiService} from "../../../services/api.service";
import {FormControl, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {AuthService} from "../../../services/auth.service";
import {NgIf} from "@angular/common";
import {RegisterService} from "../../../services/register.service";

@Component({
  selector: 'app-login',
    imports: [RouterLink, ReactiveFormsModule, NgIf],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

    authService = inject(AuthService);
    apiService = inject(ApiService);
    registerService = inject(RegisterService);
    router = inject(Router)
    errorMessage: string = "";
    formControlGroup = new FormGroup({
        email: new FormControl('', [Validators.required, Validators.email]),
        password: new FormControl('', Validators.required),
        checkbox: new FormControl(false)
    });

    submit(event: Event) {
        event.preventDefault();
        this.apiService.postData("/auth/login", this.formControlGroup.value).subscribe(res => {
            if (res['success']) {
                this.apiService.saveAccessToken(res['access_token']);
                this.authService.login();
                this.router.navigate(['']);
            } else {
                if (res['missing_steps']) {
                    this.apiService.saveAccessToken(res["access_token"]);
                    this.registerService.setStep(res['missing_steps'].at(0));
                    this.router.navigate(['auth/register']);
                } else {
                    this.formControlGroup.get("password")?.setValue("");
                    this.errorMessage = res['error'];
                }
            }
      });
    }
}
