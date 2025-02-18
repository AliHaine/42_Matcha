import {Component, inject} from '@angular/core';
import {CardService} from "../../services/card.service";
import {CardComponent} from "../card/card/card.component";
import {NgForOf} from "@angular/common";
import {NgxPaginationModule} from 'ngx-pagination';

@Component({
  selector: 'app-search',
  imports: [
    CardComponent,
    NgForOf,
    NgxPaginationModule
  ],
  templateUrl: './search.component.html',
  styleUrl: './search.component.css'
})
export class SearchComponent {

  cardService = inject(CardService)
  activeFilter = []
  p: number = 1;
  collection: any[] = [];

  constructor() {
    this.cardService.getSearchProfiles(6, 1);
  }

  addFilter() {

  }

  removeFilter() {

  }

  onPageChange(event: number) {
    this.p = event;
    this.cardService.getSearchProfiles(6, event);
  }
}
