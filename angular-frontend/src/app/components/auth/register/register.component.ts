import {Component, inject} from '@angular/core';
import {FormControl, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {RouterLink} from "@angular/router";
import {ApiService} from "../../../services/api.service";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-register',
    imports: [ReactiveFormsModule, RouterLink, NgIf],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {

    currentStep: number = 0;
    apiService = inject(ApiService);
    formControlGroupStep1 = new FormGroup({
        lastname: new FormControl('', Validators.required),
        firstname: new FormControl('', Validators.required),
        email: new FormControl('', Validators.required),
        password: new FormControl('', Validators.required),
        passwordconfirm: new FormControl('', Validators.required),
        age: new FormControl('', Validators.required),
        gender: new FormControl('male', Validators.required)
    });

    formControlGroupStep2 = new FormGroup({
        city: new FormControl('', Validators.required),
        searching: new FormControl('', Validators.required),
        commitment: new FormControl('', Validators.required),
        frequency: new FormControl('', Validators.required),

        weight: new FormControl('', Validators.required),
        size: new FormControl('', Validators.required),
        shape: new FormControl('', Validators.required),

        smoking: new FormControl('', Validators.required),
        alcohol: new FormControl('', Validators.required),
        diet: new FormControl('', Validators.required),
    });

    formControlGroupStep3 = new FormGroup({
        artCulture: new FormControl('', Validators.required),
        sportActivity: new FormControl('', Validators.required),
        other: new FormControl('', Validators.required),
        description: new FormControl('', Validators.required),
    });

    submit(event: Event, values: any) {
      event.preventDefault();
      this.currentStep++;
      console.log(values);
      this.apiService.postData('/account/register', values);
    }
}
