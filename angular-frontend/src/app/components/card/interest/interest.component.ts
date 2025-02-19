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

  /*ngOnInit() {
    if (this.interest().categoryName == "Health") {
      const a: string[] = [];
      !(this.interest().interests.at(0)) ? a.push("Don't smoke") : a.push("Smoke");
      this.interest().interests.at(1) == "Never" ? a.push("Never drink alcohol") : a.push("Drink alcohol " + this.interest().interests.at(1));
      a.push(<string>this.interest().interests.at(2));
      this.interest().interests = a;
    }
  }*/
}
