import {Component, inject, input, InputSignal} from '@angular/core';
import {ApiService} from "../../../services/api.service";

@Component({
  selector: 'app-button',
    imports: [],
  templateUrl: './button.component.html',
})
export class ButtonComponent {
  apiService = inject(ApiService);
  buttonName: InputSignal<string> = input.required();
  validator: InputSignal<boolean> = input(false);

  triggerButton() {
    this.apiService.isButtonLoading = true;
  }
}
