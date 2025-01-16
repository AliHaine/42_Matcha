import {Component, input, InputSignal} from '@angular/core';
import {Interest} from "../../../models/interest.model";

@Component({
  selector: 'app-interest',
  imports: [],
  templateUrl: './interest.component.html',
  styleUrl: './interest.component.css'
})
export class InterestComponent {
  interest: InputSignal<Interest> = input(new Interest("/icons/interest.png", "testna", ["line1", "line2", "line3"]))
}
