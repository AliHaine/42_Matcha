import {Component, inject} from '@angular/core';
import {Router, RouterLink} from "@angular/router";
import {ApiService} from "../../../services/api.service";
import {EmailValidator, FormControl, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {AuthService} from "../../../services/auth.service";

@Component({
  selector: 'app-login',
  imports: [RouterLink, ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

    authService = inject(AuthService);
    apiService = inject(ApiService);
    router = inject(Router)
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
            this.router.navigate([''])
        } else {
            console.log(res);
        }
      });
    }
}
