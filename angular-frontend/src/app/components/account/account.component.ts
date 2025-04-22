import {Component, effect, inject, signal} from '@angular/core';
import {ApiService} from "../../services/api.service";
import {AuthService} from "../../services/auth.service";
import {FormControl, FormGroup, ReactiveFormsModule} from "@angular/forms";
import {CdkTextareaAutosize} from "@angular/cdk/text-field";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {TextFieldModule} from '@angular/cdk/text-field';
import {SliderComponent} from "../utils/slider/slider.component";
import {LocationComponent} from "../utils/location/location.component";
import { PaypalComponent } from "../utils/paypal/paypal.component";
import {MatMenuModule} from '@angular/material/menu';
import {MatButtonModule} from '@angular/material/button';
import { ProfileModel } from '../../models/profile.model';
import { ProfileFactory } from '../../services/profile.factory';
import {RouterLink} from "@angular/router";
import {PopupService} from "../../services/popup.service";

@Component({
  selector: 'app-account',
  imports: [
    ReactiveFormsModule,
    CdkTextareaAutosize,
    MatFormFieldModule,
    MatInputModule,
    TextFieldModule,
    SliderComponent,
    LocationComponent,
    PaypalComponent,
    MatMenuModule,
    MatButtonModule, 
    RouterLink
],
  templateUrl: './account.component.html',
  styleUrl: './account.component.css'
})
export class AccountComponent {

  apiService = inject(ApiService);
  authService = inject(AuthService);
  popupService = inject(PopupService);
  private currentImageIndex: number = 0;
  formNumber = signal<number>(0);
  profilesView = signal<ProfileModel[]>([]);
  profileFactory = inject(ProfileFactory);
  formGroup = new FormGroup({
    firstname: new FormControl(''),
    lastname: new FormControl(''),
    city: new FormControl(''),
    age: new FormControl(''),
    gender: new FormControl(''),
    hetero: new FormControl(''),
    interests: new FormControl(''),
    username: new FormControl(''),
    email: new FormControl(''),
    password: new FormControl(''),
    description: new FormControl(''),
    picture: new FormControl(''),
    smoking: new FormControl(''),
    alcohol: new FormControl(''),
    diet: new FormControl(''),
  } as {[key: string]: any});

  constructor() {
    effect(() => {
      const profileAsDict = this.authService.currentUserProfileModel().dumpAsDict();
      if (!profileAsDict['email'])
        return;
      this.arrayConvertor(profileAsDict, profileAsDict["health"], ["smoking", "alcohol", "diet"]);
      for (let value in profileAsDict)
        if (this.formGroup.value[value] !== undefined)
          this.formGroup.controls[value].setValue(profileAsDict[value]);

    });
  }

  arrayConvertor(baseValues: {[key: string]: any}, arrayToConvert: [], values: string[]) {
    values.forEach((value, index) => {
      baseValues[value] = arrayToConvert.at(index);
    });
  }

  applyTrigger() {
    if (this.formNumber() == 3) {
      this.addPicture();
      return;
    }

    this.apiService.postData("/profiles/me", this.formGroup.value).subscribe(result => {
      if (result['disconnect'])
        this.authService.logout();
      else
        this.authService.refreshCurrentProfile()
      this.popupService.displayPopupBool(result["message"], result['success'])
    });
  }

  addPicture() {
    const pictureAsHtml = document.getElementById('picture') as HTMLInputElement;
    let file: File | undefined;

    file = pictureAsHtml.files?.[0];
    if (!file)
      return;

    const formaData = new FormData();

    formaData.append("picture", file);
    this.apiService.putData("/profiles/profile_pictures", formaData).subscribe(result => {
      this.popupService.displayPopupBool(result["message"], result['success'])
      this.formNumber.set(0);
      this.authService.refreshCurrentProfile()
    });
  }

  deletePicture() {
    this.apiService.deleteData("/profiles/profile_pictures", {"file_number": this.currentImageIndex}).subscribe(result => {
      if (result['success'])
        this.authService.refreshCurrentProfile();
      this.popupService.displayPopupBool(result["message"], result['success'])
    });
  }

  sliderTrigger(index: number) {
    this.currentImageIndex = index;
  }

  viewProfileTrigger() {
    this.apiService.getData("/profiles/me/views", {}).subscribe(result => {
      const profileModels: ProfileModel[] = [];
      for (const user of result['views']) {
        profileModels.push(this.profileFactory.getNewProfile(user));
      }
      this.profilesView.set(profileModels);
    })
  }
}
