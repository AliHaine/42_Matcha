import {Component, inject, signal} from '@angular/core';
import {ProfileModel} from "../../models/profile.model";
import {ApiService} from "../../services/api.service";
import {ActivatedRoute} from "@angular/router";
import {take} from "rxjs";

@Component({
  selector: 'app-profile',
  imports: [],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css'
})
export class ProfileComponent {

  apiService = inject(ApiService);
  route = inject(ActivatedRoute);
  profile = signal<ProfileModel>(new ProfileModel({}));

  constructor() {
    this.route.paramMap.pipe(take(1)).subscribe(params => {
      this.apiService.getData(`/profiles/${params.get('id')}`, {}).subscribe(profile => {
        this.profile.set(new ProfileModel(profile['user']));
      })
    })
  }
}
