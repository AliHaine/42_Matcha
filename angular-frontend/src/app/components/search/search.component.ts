import {Component, inject} from '@angular/core';
import {CardComponent} from "../card/card/card.component";
import {NgForOf} from "@angular/common";
import {NgxPaginationModule} from 'ngx-pagination';
import {SearchService} from "../../services/search.service";

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

  searchService = inject(SearchService);
  activeFilter = []
  p: number = 1;
  collection: any[] = [];

  constructor() {
    this.searchService.getSearchProfiles(1);
  }

  addFilter() {

  }

  removeFilter() {

  }

  onPageChange(event: number) {
    this.p = event;
    this.searchService.getSearchProfiles(event);
  }
}
