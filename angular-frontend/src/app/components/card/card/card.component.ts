import {Component, inject, input, InputSignal} from '@angular/core';
import {CardModel} from "../../../models/card.model";
import {InterestComponent} from "../interest/interest.component";
import {RouterLink} from "@angular/router";
import {ApiService} from "../../../services/api.service";

@Component({
  selector: 'app-card',
  imports: [
    InterestComponent,
    RouterLink
  ],
  templateUrl: './card.component.html',
  styleUrl: './card.component.css'
})

export class CardComponent {
  card: InputSignal<CardModel> = input.required();
  apiService = inject(ApiService);

  likeUser() {
    this.apiService.postData(`/profiles/${this.card().userId}`, {action: 'like',}).subscribe((response) => {
      console.log(response);
    })
  }
}
