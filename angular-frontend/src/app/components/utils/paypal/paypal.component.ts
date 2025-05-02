import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgxPayPalModule, IPayPalConfig, ICreateOrderRequest } from 'ngx-paypal';
import { ApiService } from '../../../services/api.service';
import { AuthService } from '../../../services/auth.service';
import { PopupService } from '../../../services/popup.service';


@Component({
  selector: 'app-paypal',
  standalone: true,
  imports: [CommonModule, NgxPayPalModule],
  templateUrl: './paypal.component.html',
  styleUrl: './paypal.component.css'
})
export class PaypalComponent implements OnInit  {

  public payPalConfig?: IPayPalConfig;
  private apiService = inject(ApiService);
  private authService = inject(AuthService);
  private popupService = inject(PopupService);

  ngOnInit(): void {
    this.initConfig();
  }

  private initConfig(): void {
    this.payPalConfig = {
      currency: 'USD',
      clientId: 'AUrAFVVvKsLQjKchsSjouvZc2MPf5M0YKeTW0nIak2I4_ucDaJZaPJ28akmG4jQ5UUVml6vVhAji0ul-',
      createOrderOnClient: (data) => <ICreateOrderRequest>{
        intent: 'CAPTURE',
        purchase_units: [{
          amount: {
            currency_code: 'USD',
            value: '10.00',
          }
        }]
      },
      advanced: {
        commit: 'true',
        extraQueryParams: [
          { name: 'disable-funding', value: 'card,venmo' }
        ]
      },
      style: {
        layout: 'vertical'
      },
      onApprove: (_, actions) => {
        actions.order.capture().then((_: any) => {
          this.premium();
        });
      },
      onClientAuthorization: (_) => {
      },
      onCancel: (data, actions) => {
        this.popupService.displayPopupBool("Transaction canceled", false);
      },
      onError: err => {
        console.log('PayPal Error');
      }
    };
  }

  premium() {
    this.apiService.postData("/profiles/me/premium", {}).subscribe(result => {
      this.popupService.displayPopupBool("You are now premium", true);
      this.authService.refreshCurrentProfile();
    });
  }

}
