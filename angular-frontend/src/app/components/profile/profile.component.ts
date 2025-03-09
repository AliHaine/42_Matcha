import {Component, inject, signal} from '@angular/core';
import {ProfileModel} from "../../models/profile.model";
import {ApiService} from "../../services/api.service";
import {ActivatedRoute, Router} from "@angular/router";
import {take} from "rxjs";
import {ProfileFactory} from "../../services/profile.factory";
import {NgForOf} from "@angular/common";
import {SliderComponent} from "../utils/slider/slider.component";

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
  route = inject(ActivatedRoute);
  router = inject(Router)
  profile = signal<ProfileModel>(new ProfileModel({}));
  profileFactory = inject(ProfileFactory);

  constructor() {
    this.route.paramMap.pipe(take(1)).subscribe(params => {
      this.apiService.getData(`/profiles/${params.get('id')}`, {}).subscribe(profile => {
        console.log(profile)
        this.profile.set(this.profileFactory.getNewProfile(profile['user']));
      })
    })
  }

  sendMessageTrigger() {
    //Need to active the chat with this user
    this.router.navigate(['chat'])
  }
}
