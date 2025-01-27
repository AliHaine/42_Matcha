import {Component, input, InputSignal, OnInit} from '@angular/core';
import {CardModel} from "../../../models/card.model";
import {InterestComponent} from "../interest/interest.component";

@Component({
  selector: 'app-card',
  imports: [
    InterestComponent
  ],
  templateUrl: './card.component.html',
  styleUrl: './card.component.css'
})

export class CardComponent implements OnInit {
  card: InputSignal<CardModel> = input.required();

  constructor() {
    console.log("constructor called")
  }

  ngOnInit() {
    console.log("on init called")
  }


}
