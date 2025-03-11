import {Component, inject, input, InputSignal} from '@angular/core';
import {RouterLink} from "@angular/router";
import {ApiService} from "../../../services/api.service";
import {ProfileModel} from "../../../models/profile.model";

@Component({
  selector: 'app-card',
  imports: [
    RouterLink,
  ],
  templateUrl: './card.component.html',
  styleUrl: './card.component.css'
})

export class CardComponent {
  profile: InputSignal<ProfileModel> = input.required();
  apiService = inject(ApiService);

  likeUser() {
    this.apiService.postData(`/profiles/${this.profile().userId}`, {action: 'like',}).subscribe((response) => {
      console.log(response);
    })
  }
}
