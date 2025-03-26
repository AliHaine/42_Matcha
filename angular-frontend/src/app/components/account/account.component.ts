import {Component, inject, signal} from '@angular/core';
import {ApiService} from "../../services/api.service";
import {AuthService} from "../../services/auth.service";
import {FormControl, FormGroup, ReactiveFormsModule} from "@angular/forms";
import {NgIf} from "@angular/common";
import {LocationService} from "../../services/location.service";
import {CdkTextareaAutosize} from "@angular/cdk/text-field";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {TextFieldModule} from '@angular/cdk/text-field';
import {SliderComponent} from "../utils/slider/slider.component";
import {ProfileModel} from "../../models/profile.model";
import {ProfileFactory} from "../../services/profile.factory";
import {LocationComponent} from "../location/location.component";

@Component({
  selector: 'app-account',
  imports: [
    ReactiveFormsModule,
    CdkTextareaAutosize,
    MatFormFieldModule,
    MatInputModule,
    TextFieldModule,
    NgIf,
    SliderComponent,
    LocationComponent,
  ],
  templateUrl: './account.component.html',
  styleUrl: './account.component.css'
})
export class AccountComponent {

  apiService = inject(ApiService);
  authService = inject(AuthService);
  profileFactory = inject(ProfileFactory);
  placeHolderMessage: string = "";
  profile = signal<ProfileModel>(new ProfileModel({}));
  private currentImageIndex: number = 0;
  formGroup = new FormGroup({
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
    smoking: new FormControl(''),
    alcohol: new FormControl(''),
    diet: new FormControl(''),
  } as {[key: string]: any});

  constructor() {
    this.apiService.getData("/profiles/me", {}).subscribe(result => {
      this.profile.set(this.profileFactory.getNewProfile(result["user"]));
      console.log(result['user']);

      this.arrayConvertor(result['user'], result["user"]["health"], ["smoking", "alcohol", "diet"]);

      for (let value in result["user"])
        if (this.formGroup.value[value] !== undefined)
          this.formGroup.controls[value].setValue(result["user"][value]);
    })
  }

  arrayConvertor(baseValues: {[key: string]: any}, arrayToConvert: [], values: string[]) {
    values.forEach((value, index) => {
      baseValues[value] = arrayToConvert.at(index);
    });
  }

  applyTrigger() {
    const pictureAsHtml = document.getElementById('picture') as HTMLInputElement;
    let file: File | undefined;

    file = pictureAsHtml.files?.[0];
    if (file)
      this.addPicture(file);

    this.apiService.postData("/profiles/me", this.formGroup.value).subscribe(result => {
      if (result['disconnect'])
        this.authService.logout();
      if (!result['success'])
        this.placeHolderMessage = result['error'];
      else
        this.placeHolderMessage = "Successfully updated";
    });
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
    this.apiService.deleteData("/profiles/profile_pictures", {"file_number": this.currentImageIndex}).subscribe(result => {
      console.log(result);
    })
  }

  sliderTrigger(index: number) {
    this.currentImageIndex = index;
  }
}
