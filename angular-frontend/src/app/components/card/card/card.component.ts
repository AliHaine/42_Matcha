import {Component, input, InputSignal} from '@angular/core';
import {Card} from "../../../models/card.model";
import {InterestComponent} from "../interest/interest.component";

@Component({
  selector: 'app-card',
  imports: [
    InterestComponent
  ],
  templateUrl: './card.component.html',
  styleUrl: './card.component.css'
})

export class CardComponent {
  card: InputSignal<Card> = input.required();
}
