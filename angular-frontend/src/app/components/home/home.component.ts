import {Component, inject} from '@angular/core';
import {CardComponent} from "../card/card/card.component";
import {CardService} from "../../services/card.service";
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-home',
  imports: [CardComponent, NgForOf],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent{
  cardService = inject(CardService);

  constructor() {
    console.log("home called")
  }
}
