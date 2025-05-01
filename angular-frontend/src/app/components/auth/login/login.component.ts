import {Component, inject, signal} from '@angular/core';
import {Router, RouterLink} from "@angular/router";
import {ApiService} from "../../../services/api.service";
import {FormControl, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {AuthService} from "../../../services/auth.service";
import {RegisterService} from "../../../services/register.service";
import { PopupService } from '../../../services/popup.service';
import {ButtonComponent} from "../../utils/button/button.component";

@Component({
  selector: 'app-login',
    imports: [RouterLink, ReactiveFormsModule, ButtonComponent],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

    authService = inject(AuthService);
    apiService = inject(ApiService);
    registerService = inject(RegisterService);
    router = inject(Router)
    popupService = inject(PopupService);
    formNumber = signal<number>(0);
    formControlGroup = new FormGroup({
        username: new FormControl('', Validators.required),
        password: new FormControl('', Validators.required),
        checkbox: new FormControl(false)
    });
    resetmail = new FormControl('', Validators.email);

    submit(event: Event) {
        event.preventDefault();
        this.apiService.postData("/auth/login", this.formControlGroup.value).subscribe(result => {
            if (result['success']) {
                this.apiService.saveAccessToken(result['access_token']);
                this.authService.login();
                this.router.navigate(['']);
            } else {
                if (result['missing_steps']) {
                    this.apiService.saveAccessToken(result["access_token"]);
                    this.registerService.setStep(result['missing_steps'].at(0));
                    this.router.navigate(['auth/register']);
                } else
                    this.formControlGroup.get("password")?.setValue("");
            }
            this.popupService.displayPopupBool(result['message'], result['success']);
            this.apiService.isButtonLoading = false;
      });
    }

    submitForgot(event: Event) {
        event.preventDefault();
        this.apiService.postData("/auth/get_reset_password", {email: this.resetmail.value}).subscribe(result => {
            this.popupService.displayPopupBool(result['message'], result['success']);
            this.apiService.isButtonLoading = false;
        });
    }
}
