import {Component, inject, signal} from '@angular/core';
import {CardComponent} from "../card/card/card.component";
import {NgForOf} from "@angular/common";
import {NgxPaginationModule} from 'ngx-pagination';
import {SearchService} from "../../services/search.service";
import {MatSlider, MatSliderRangeThumb} from '@angular/material/slider';
import {FormControl, FormGroup, ReactiveFormsModule} from "@angular/forms";
import {LocationComponent} from "../utils/location/location.component";
import {MatMenu, MatMenuItem, MatMenuTrigger} from "@angular/material/menu";
import {RouterLink} from "@angular/router";
import {MatIconButton} from "@angular/material/button";
import {LoadingComponent} from "../loading/loading.component";

@Component({
  selector: 'app-search',
    imports: [
        CardComponent,
        NgForOf,
        NgxPaginationModule,
        MatSlider,
        MatSliderRangeThumb,
        ReactiveFormsModule,
        LocationComponent,
        MatMenu,
        MatMenuItem,
        MatMenuTrigger,
        LoadingComponent
    ],
  templateUrl: './search.component.html',
  styleUrl: './search.component.css'
})
export class SearchComponent {

  searchService = inject(SearchService);
  p = signal<number>(1);
  formGroup = new FormGroup({
    ageMin: new FormControl(15),
    ageMax: new FormControl(80),
    location: new FormControl(''),
    interest: new FormControl(''),
    sortOrder: new FormControl('ASC'),
    sortBy: new FormControl(''),
  })

  constructor() {
    this.updateSearch(1);
  }

  updateSearch(page: number) {
    this.p.set(page);
    this.searchService.getSearchProfiles(Object.assign({"page": page}, this.formGroup.value));
  }

  sortBy(value: string) {
    this.formGroup.value.sortBy = value;
  }
}
