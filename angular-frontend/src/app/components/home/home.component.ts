import {Component, inject} from '@angular/core';
import {CardComponent} from "../card/card/card.component";
import {CardService} from "../../services/card.service";

@Component({
  selector: 'app-home',
  imports: [CardComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  cardService = inject(CardService);
}
