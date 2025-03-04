import {Component, inject} from '@angular/core';
import {ApiService} from "../../services/api.service";
import {AuthService} from "../../services/auth.service";
import {FormControl, FormGroup, ReactiveFormsModule} from "@angular/forms";
import {NgForOf, NgIf} from "@angular/common";
import {LocationService} from "../../services/location.service";
import {CdkTextareaAutosize} from "@angular/cdk/text-field";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {TextFieldModule} from '@angular/cdk/text-field';

@Component({
  selector: 'app-account',
  imports: [
    ReactiveFormsModule,
    NgForOf,
    CdkTextareaAutosize,
    MatFormFieldModule,
    MatInputModule,
    TextFieldModule,
    NgIf
  ],
  templateUrl: './account.component.html',
  styleUrl: './account.component.css'
})
export class AccountComponent {

  apiService = inject(ApiService);
  authService = inject(AuthService);
  locationService = inject(LocationService);
  errorMessage: string = "Error msg example";
  formGroup: FormGroup = new FormGroup({
    firstname: new FormControl(''),
    lastname: new FormControl(''),
    city: new FormControl(''),
    age: new FormControl(''),
    gender: new FormControl(''),
    hetero: new FormControl(''),
    interests: new FormControl(''),
    email: new FormControl(''),
    password: new FormControl(''),
    description: new FormControl(''),
  } as {[key: string]: any});

  constructor() {
    this.apiService.getData("/profiles/me", {}).subscribe(result => {
      for (const value in result["user"])
        if (this.formGroup.value[value] !== undefined)
          this.formGroup.controls[value].setValue(result["user"][value]);
    })
    this.locationService.observableToSubscribe(this.formGroup.controls["city"].valueChanges)
  }

  applyTrigger() {
    console.log(this.formGroup.value)
    this.apiService.postData("/profiles/me", this.formGroup.value).subscribe(result => {
      console.log(result);
      if (result['disconnect'])
        this.authService.logout();
    });
  }

  setLocation(name: string) {
    this.formGroup.controls["city"].setValue(name);
  }
}
