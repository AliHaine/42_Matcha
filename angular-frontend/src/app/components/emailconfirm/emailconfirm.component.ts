import {Component, inject} from '@angular/core';
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-emailconfirm',
  imports: [],
  templateUrl: './emailconfirm.component.html',
  styleUrl: './emailconfirm.component.css'
})
export class EmailconfirmComponent {
  route = inject(ActivatedRoute);

  confirmationTrigger(event: Event): void {
    event.preventDefault();
    const token = this.route.snapshot.paramMap.get('token');
    console.log(token)
  }

}
