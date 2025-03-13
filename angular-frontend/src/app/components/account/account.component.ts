import {Component, inject, signal} from '@angular/core';
import {ApiService} from "../../services/api.service";
import {AuthService} from "../../services/auth.service";
import {FormControl, FormGroup, ReactiveFormsModule} from "@angular/forms";
import {NgForOf, NgIf} from "@angular/common";
import {LocationService} from "../../services/location.service";
import {CdkTextareaAutosize} from "@angular/cdk/text-field";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {TextFieldModule} from '@angular/cdk/text-field';
import {SliderComponent} from "../utils/slider/slider.component";
import {ProfileModel} from "../../models/profile.model";
import {ProfileFactory} from "../../services/profile.factory";

@Component({
  selector: 'app-account',
  imports: [
    ReactiveFormsModule,
    NgForOf,
    CdkTextareaAutosize,
    MatFormFieldModule,
    MatInputModule,
    TextFieldModule,
    NgIf,
    SliderComponent,
  ],
  templateUrl: './account.component.html',
  styleUrl: './account.component.css'
})
export class AccountComponent {

  apiService = inject(ApiService);
  authService = inject(AuthService);
  locationService = inject(LocationService);
  profileFactory = inject(ProfileFactory);
  placeHolderMessage: string = "";
  profile = signal<ProfileModel>(new ProfileModel({}));
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
    picture: new FormControl(''),
  } as {[key: string]: any});

  constructor() {
    this.apiService.getData("/profiles/me", {}).subscribe(result => {
      this.profile.set(this.profileFactory.getNewProfile(result["user"]));
      for (const value in result["user"])
        if (this.formGroup.value[value] !== undefined)
          this.formGroup.controls[value].setValue(result["user"][value]);
    })
    this.locationService.observableToSubscribe(this.formGroup.controls["city"].valueChanges)
  }

  applyTrigger() {
    const pictureAsHtml = document.getElementById('picture') as HTMLInputElement;
    let file: File | undefined;

    file = pictureAsHtml.files?.[0];
    if (file)
      this.addPicture(file);

    this.apiService.postData("/profiles/me", this.formGroup.value).subscribe(result => {
      console.log(result);
      if (result['disconnect'])
        this.authService.logout();
      if (!result['success'])
        this.placeHolderMessage = result['error'];
      else
        this.placeHolderMessage = "Successfully updated";
    });
  }

  setLocation(name: string) {
    this.formGroup.controls["city"].setValue(name);
  }

  keyPressed() {
    this.placeHolderMessage = "";
  }

  addPicture(file: File) {
    const formaData = new FormData();

    formaData.append("picture", file);
    this.apiService.putData("/profiles/profile_pictures", formaData).subscribe(result => {
      console.log(result);
    });
  }

  deletePicture() {
    this.apiService.deleteData("/profiles/profile_pictures", {"file_number": 0}).subscribe(result => {
      console.log(result);
    })
  }
}
