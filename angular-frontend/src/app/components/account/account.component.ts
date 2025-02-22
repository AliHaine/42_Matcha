import {Component, inject} from '@angular/core';
import {ApiService} from "../../services/api.service";
import {AuthService} from "../../services/auth.service";
import {FormControl, FormGroup, ReactiveFormsModule} from "@angular/forms";
import {NgForOf} from "@angular/common";
import {LocationService} from "../../services/location.service";
import {CdkTextareaAutosize} from "@angular/cdk/text-field";
import {MatFormField} from "@angular/material/form-field";
import {MatInput} from "@angular/material/input";
import {TextFieldModule} from '@angular/cdk/text-field';

@Component({
  selector: 'app-account',
  imports: [
    ReactiveFormsModule,
    NgForOf,
    CdkTextareaAutosize,
    MatFormField,
    MatInput,
    TextFieldModule
  ],
  templateUrl: './account.component.html',
  styleUrl: './account.component.css'
})
export class AccountComponent {

  apiService = inject(ApiService);
  authService = inject(AuthService);
  locationService = inject(LocationService);
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
      console.log(this.formGroup.value["city"])
      for (const value in result["user"])
        if (this.formGroup.value[value] !== undefined)
          this.formGroup.controls[value].setValue(result["user"][value]);
    })
    this.locationService.observableToSubscribe(this.formGroup.controls["city"].valueChanges)
  }

  applyTrigger() {
    console.log(this.formGroup.value)
  }

  setLocation(name: string) {
    this.formGroup.controls["city"].setValue(name);
  }
}
