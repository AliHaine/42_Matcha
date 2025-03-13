import {Component, input, InputSignal} from '@angular/core';
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-slider',
  imports: [
    NgIf,
  ],
  templateUrl: './slider.component.html',
  styleUrl: './slider.component.css'
})
export class SliderComponent {
  images: InputSignal<string[]> = input.required();
  currentIndex: number = 0;

  arrowLeftClick() {
    this.currentIndex--;
    if (this.currentIndex < 0)
      this.currentIndex = this.images().length-1;
  }

  arrowRightClick() {
    this.currentIndex++;
    if (this.currentIndex > this.images().length-1)
      this.currentIndex = 0;
  }
}
