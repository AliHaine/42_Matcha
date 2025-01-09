import {Component, inject, ViewChild, ViewContainerRef} from '@angular/core';
import {CardComponent} from "../card/card.component";

@Component({
  selector: 'app-root',
  imports: [CardComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

}
