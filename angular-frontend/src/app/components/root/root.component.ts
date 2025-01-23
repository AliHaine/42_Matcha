import { Component } from '@angular/core';
import {PageComponent} from "../page/page.component";
import {RouterOutlet} from "@angular/router";

@Component({
  selector: 'app-root',
  imports: [
    PageComponent,
    RouterOutlet,
  ],
  templateUrl: './root.component.html',
})
export class RootComponent {}
