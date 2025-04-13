import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgxPayPalModule, IPayPalConfig, ICreateOrderRequest } from 'ngx-paypal';
import { ApiService } from '../../services/api.service';
import { AuthService } from '../../services/auth.service';


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
        commit: 'true'
      },
      style: {
        layout: 'vertical'
      },
      onApprove: (data, actions) => {
        console.log('Transaction approved', data);
        actions.order.capture().then((details: any) => {
          console.log('Transaction completed!', details);
          this.premium();
        });
      },
      onClientAuthorization: (data) => {
        console.log('Client Authorization:', data);
      },
      onCancel: (data, actions) => {
        console.log('Transaction canceled', data);
      },
      onError: err => {
        console.log('PayPal Error', err);
      }
    };
  }

  premium() {
    this.apiService.postData("/profiles/me/premium", {}).subscribe(result => {
      console.log(result);
      this.authService.refreshCurrentProfile();
    });
  }

}
