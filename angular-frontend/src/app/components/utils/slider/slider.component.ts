import {Component, input, InputSignal, OnInit} from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";
import {IconModel} from "../../../models/icon.model";

@Component({
  selector: 'app-slider',
  imports: [
    NgIf,
    NgForOf
  ],
  templateUrl: './slider.component.html',
  styleUrl: './slider.component.css'
})
export class SliderComponent implements OnInit {
  images: InputSignal<string[]> = input.required();
  icons = input<IconModel[] | undefined>();
  currentImagePath: string = "";
  currentIndex: number = 0;

  ngOnInit(): void {
    this.currentImagePath = <string>this.images().at(0);
  }

  arrowLeftClick() {
    this.currentIndex--;
    if (this.currentIndex < 0)
      this.currentIndex = this.images().length-1;
    this.currentImagePath = this.images()[this.currentIndex];
  }

  arrowRightClick() {
    this.currentIndex++;
    if (this.currentIndex > this.images().length-1)
      this.currentIndex = 0;
    this.currentImagePath = this.images()[this.currentIndex];
  }
}
