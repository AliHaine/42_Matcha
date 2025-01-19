import { Component } from '@angular/core';

@Component({
  selector: 'app-page',
  imports: [],
  templateUrl: './page.component.html',
  styleUrl: './page.component.css'
})
export class PageComponent {

    title: String;
    content: String;

    constructor(title: String, content: String) {
      this.title = title;
      this.content = content;
    }
}
