import {Component, input, InputSignal} from '@angular/core';
import {CardModel} from "../../../models/card.model";
import {InterestComponent} from "../interest/interest.component";
import {RouterLink} from "@angular/router";

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
}
