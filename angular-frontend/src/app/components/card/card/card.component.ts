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
  private interests: {} = {
    "interest": ["line1", "line2", "line3"],
    "health": ["line1", "line2", "line3"],
    "shape": ["line1", "line2", "line3"],
    "looking": ["line1", "line2", "line3"]
  };

  card: InputSignal<Card> = input(new Card("test", "test", this.interests, "test"));
}
