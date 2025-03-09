import {Component, inject, signal} from '@angular/core';
import {ProfileModel} from "../../models/profile.model";
import {ApiService} from "../../services/api.service";
import {ActivatedRoute} from "@angular/router";
import {take} from "rxjs";
import {ProfileFactory} from "../../services/profile.factory";
import {NgForOf} from "@angular/common";
import {SliderComponent} from "../utils/slider/slider.component";
import {IconService} from "../../services/icon.service";

@Component({
  selector: 'app-profile',
  imports: [
    NgForOf,
    SliderComponent
  ],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css'
})
export class ProfileComponent {

  apiService = inject(ApiService);
  iconService = inject(IconService);
  route = inject(ActivatedRoute);
  profile = signal<ProfileModel>(new ProfileModel({}));
  profileFactory = inject(ProfileFactory);

  constructor() {
    this.route.paramMap.pipe(take(1)).subscribe(params => {
      this.apiService.getData(`/profiles/${params.get('id')}`, {}).subscribe(profile => {
        this.profile.set(this.profileFactory.getNewProfile(profile['user']));
      })
    })
  }
}
