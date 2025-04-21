import {inject, Component} from '@angular/core';
import {PopupService} from "../../../services/popup.service";

@Component({
  selector: 'app-popup',
  imports: [],
  templateUrl: './popup.component.html',
  styleUrl: './popup.component.css'
})
export class PopupComponent {

  popupService = inject(PopupService);
}
