import {Component, inject, ViewChild, ViewContainerRef} from '@angular/core';
import {CardComponent} from "../card/card.component";
import {NavbarComponent} from "../navbar/navbar.component";

@Component({
  selector: 'app-root',
  imports: [CardComponent, NavbarComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

}
