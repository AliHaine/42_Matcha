import {Component, inject} from '@angular/core';
import {CardComponent} from "../card/card/card.component";
import {NavbarComponent} from "../navbar/navbar.component";
import {FooterComponent} from "../footer/footer.component";
import {CardService} from "../../services/card.service";

@Component({
  selector: 'app-root',
  imports: [CardComponent, NavbarComponent, FooterComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  cardService = inject(CardService);
}
