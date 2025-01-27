import {Component, input, InputSignal} from '@angular/core';
import {InterestModel} from "../../../models/interest.model";

@Component({
  selector: 'app-interest',
  imports: [],
  templateUrl: './interest.component.html',
  styleUrl: './interest.component.css'
})
export class InterestComponent {
  interest: InputSignal<InterestModel> = input.required();
}
