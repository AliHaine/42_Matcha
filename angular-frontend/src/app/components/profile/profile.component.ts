import {Component, inject, signal} from '@angular/core';
import {ProfileModel} from "../../models/profile.model";
import {ApiService} from "../../services/api.service";
import {ActivatedRoute, Router} from "@angular/router";
import {take} from "rxjs";
import {ProfileFactory} from "../../others/profile.factory";
import {CardimageComponent} from "../cardimage/cardimage.component";
import {LoadingComponent} from "../loading/loading.component";
import {PopupService} from "../../services/popup.service";

@Component({
  selector: 'app-profile',
  imports: [
    CardimageComponent,
    LoadingComponent
  ],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css',
})
export class ProfileComponent {

  apiService = inject(ApiService);
  popupService = inject(PopupService);
  route = inject(ActivatedRoute);
  router = inject(Router)
  profile = signal<ProfileModel | undefined>(undefined);
  profileFactory = inject(ProfileFactory);

  constructor() {
    this.route.paramMap.pipe(take(1)).subscribe(params => {
      this.apiService.getData(`/profiles/${params.get('id')}`, {}).subscribe(profile => {
        if (!profile['success']) {
          this.popupService.displayPopupBool(profile['message'], profile['success'])
          this.router.navigate(['/']);
          return;
        }
        this.profile.set(this.profileFactory.getNewProfile(profile['user']));
      })
    })
  }
}
