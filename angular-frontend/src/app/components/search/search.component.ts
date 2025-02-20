import {Component, inject} from '@angular/core';
import {CardComponent} from "../card/card/card.component";
import {NgForOf} from "@angular/common";
import {NgxPaginationModule} from 'ngx-pagination';
import {SearchService} from "../../services/search.service";
import {MatSlider, MatSliderRangeThumb} from '@angular/material/slider';
import {FormControl, FormGroup, ReactiveFormsModule} from "@angular/forms";

@Component({
  selector: 'app-search',
  imports: [
    CardComponent,
    NgForOf,
    NgxPaginationModule,
    MatSlider,
    MatSliderRangeThumb,
    ReactiveFormsModule
  ],
  templateUrl: './search.component.html',
  styleUrl: './search.component.css'
})
export class SearchComponent {

  searchService = inject(SearchService);
  p: number = 1;
  formGroup = new FormGroup({
    ageMin: new FormControl(15),
    ageMax: new FormControl(80),
    location: new FormControl(''),
    interest: new FormControl(''),
    fameRate: new FormControl(false),
  })

  constructor() {
    this.updateSearch(1);
  }

  updateSearch(page: number) {
    this.p = page;
    this.searchService.getSearchProfiles(Object.assign({"page": page}, this.formGroup.value));
  }
}
