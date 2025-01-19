import { Injectable } from '@angular/core';
import {PageComponent} from "../components/page/page.component";

@Injectable({
  providedIn: 'root'
})
export class PageService {

  pages: [PageComponent] = [];

  constructor() {
    this.pages.push(new PageComponent("test", "salut"))
  }
}
