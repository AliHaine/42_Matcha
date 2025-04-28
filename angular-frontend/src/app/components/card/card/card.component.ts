import {ChangeDetectionStrategy, Component, inject, input, InputSignal} from '@angular/core';
import {InterestComponent} from "../interest/interest.component";
import {RouterLink} from "@angular/router";
import {ApiService} from "../../../services/api.service";
import {ProfileModel} from "../../../models/profile.model";
import {CardimageComponent} from "../../cardimage/cardimage.component";

@Component({
  selector: 'app-card',
  imports: [
    InterestComponent,
    RouterLink,
    CardimageComponent,
  ],
  templateUrl: './card.component.html',
  styleUrl: './card.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class CardComponent {
  profile: InputSignal<ProfileModel> = input.required();
  apiService = inject(ApiService);
}
