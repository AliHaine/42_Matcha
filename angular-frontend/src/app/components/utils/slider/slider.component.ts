import {Component, EventEmitter, input, InputSignal, Output} from '@angular/core';

@Component({
  selector: 'app-slider',
  imports: [],
  templateUrl: './slider.component.html',
  styleUrl: './slider.component.css'
})
export class SliderComponent {
  images: InputSignal<string[]> = input.required();
  @Output() currentIndexEvent = new EventEmitter<number>();
  currentIndex: number = 0;

  arrowLeftClick() {
    this.currentIndex--;
    if (this.currentIndex < 0)
      this.currentIndex = this.images().length-1;
    this.currentIndexEvent.emit(this.currentIndex);
  }

  arrowRightClick() {
    this.currentIndex++;
    if (this.currentIndex > this.images().length-1)
      this.currentIndex = 0;
    this.currentIndexEvent.emit(this.currentIndex);
  }
}
