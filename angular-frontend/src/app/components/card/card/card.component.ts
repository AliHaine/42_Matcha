import {Component, input, InputSignal} from '@angular/core';
import {Card} from "../../../models/card.model";

@Component({
  selector: 'app-card',
  imports: [],
  templateUrl: './card.component.html',
  styleUrl: './card.component.css'
})
export class CardComponent {

  card: InputSignal<Card> = input(new Card("test", "test", [], "test"))
}
