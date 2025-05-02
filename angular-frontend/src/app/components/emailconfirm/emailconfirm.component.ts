import {Component, inject} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {ApiService} from "../../services/api.service";
import {ButtonComponent} from "../utils/button/button.component";
import { PopupService } from '../../services/popup.service';

@Component({
  selector: 'app-emailconfirm',
  imports: [
    ButtonComponent
  ],
  templateUrl: './emailconfirm.component.html',
})
export class EmailconfirmComponent {
  route = inject(ActivatedRoute);
  router = inject(Router);
  apiService = inject(ApiService);
  popupService = inject(PopupService);

  confirmationTrigger(event: Event): void {
    event.preventDefault();
    const token = this.route.snapshot.paramMap.get('token');
    this.apiService.postData("/auth/confirm_email", {token: token}).subscribe(result => {
      if (result["success"]) {
        this.router.navigate(['/']);
        this.popupService.displayPopupBool(result['message'], result['success']);
        this.apiService.isButtonLoading = false;
      }
    });
  }
}
