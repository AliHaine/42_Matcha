import {Component, inject, ViewChild, ViewContainerRef} from '@angular/core';
import {CardComponent} from "../card/card.component";

@Component({
  selector: 'app-root',
  imports: [],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  @ViewChild('CardComponent', { read: ViewContainerRef, static: true })
  private container!: ViewContainerRef;

  public injectTest() {
    const cardRef = this.container.createComponent(CardComponent);
    console.log('Card injected:', cardRef);
}
}
