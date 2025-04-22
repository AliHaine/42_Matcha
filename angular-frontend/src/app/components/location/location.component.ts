import {Component, inject, input, InputSignal, OnInit} from '@angular/core';
import {LocationService} from "../../services/location.service";
import {FormControl} from "@angular/forms";

@Component({
  selector: 'app-location',
  imports: [],
  templateUrl: './location.component.html',
  styleUrl: './location.component.css'
})
export class LocationComponent implements OnInit {
  locationService = inject(LocationService);
  cityFormControl: InputSignal<FormControl> = input.required();

  ngOnInit(): void {
     this.locationService.observableToSubscribe(this.cityFormControl().valueChanges);
  }

  setLocation(value: string) {
      this.cityFormControl().setValue(value);
  }
}
