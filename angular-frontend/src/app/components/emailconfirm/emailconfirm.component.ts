import {Component, inject} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {ApiService} from "../../services/api.service";

@Component({
  selector: 'app-emailconfirm',
  imports: [],
  templateUrl: './emailconfirm.component.html',
  styleUrl: './emailconfirm.component.css'
})
export class EmailconfirmComponent {
  route = inject(ActivatedRoute);
  router = inject(Router);
  apiService = inject(ApiService);

  confirmationTrigger(event: Event): void {
    event.preventDefault();
    const token = this.route.snapshot.paramMap.get('token');
    this.apiService.postData("/auth/confirm_email", {token: token}).subscribe(result => {
      if (result["success"]) {
        this.router.navigate(['/']);
      }
      console.log(result);
    });
  }

  resendEmail(event: Event): void {
    event.preventDefault();
    this.apiService.postData("/auth/resend_email", {});
  }
}
