import { Component, inject } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import { ApiService } from '../../services/api.service';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from "@angular/forms";
import { Router } from '@angular/router';
import {PopupService} from "../../services/popup.service";
import {ButtonComponent} from "../utils/button/button.component";

@Component({
  selector: 'app-forgotpass',
  imports: [ReactiveFormsModule, ButtonComponent],
  templateUrl: './forgotpass.component.html',
  styleUrl: './forgotpass.component.css'
})
export class ForgotpassComponent {
  apiService = inject(ApiService);
  popupService = inject(PopupService);
  router = inject(Router);
  route = inject(ActivatedRoute);

  formGroupForgot = new FormGroup({
    password: new FormControl('', Validators.required),
    passwordConfirm: new FormControl('', Validators.required)
  })

  submit(event: Event): void {
    event.preventDefault();
    const token = this.route.snapshot.paramMap.get("token");
    this.apiService.postData("/auth/reset_password", {token: token, password: this.formGroupForgot.value.password}).subscribe(result => {
      this.popupService.displayPopupBool(result['message'], result['success']);
      this.apiService.isButtonLoading = false;
      if (result["success"]) {
        this.router.navigate(['/login'])
      }
    })
  }
}