import {Component, inject, input, InputSignal} from '@angular/core';
import {InterestComponent} from "../interest/interest.component";
import {RouterLink} from "@angular/router";
import {ApiService} from "../../../services/api.service";
import {ProfileModel} from "../../../models/profile.model";
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-card',
  imports: [
    InterestComponent,
    RouterLink,
    NgForOf,
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
