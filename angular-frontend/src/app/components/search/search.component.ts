import {Component, inject} from '@angular/core';
import {CardService} from "../../services/card.service";
import {CardComponent} from "../card/card/card.component";
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-search',
  imports: [
    CardComponent,
    NgForOf
  ],
  templateUrl: './search.component.html',
  styleUrl: './search.component.css'
})
export class SearchComponent {

  cardService = inject(CardService)
  activeFilter = []

  addFilter() {

  }

  removeFilter() {

  }
}
