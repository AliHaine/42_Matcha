import {Component, inject, input, InputSignal} from '@angular/core';
import {ProfileModel} from "../../models/profile.model";
import {ProfileActionService} from "../../services/profileaction.service";
import {SvgIconService} from "../../services/svg-icon.service";
import { MatIconModule } from '@angular/material/icon';
import {Router} from "@angular/router";
import {MatMenu, MatMenuItem, MatMenuTrigger} from "@angular/material/menu";

@Component({
  selector: 'app-cardimage',
    imports: [
        MatIconModule,
        MatMenuTrigger,
        MatMenu,
        MatMenuItem
    ],
  templateUrl: './cardimage.component.html',
  styleUrl: './cardimage.component.css'
})
export class CardimageComponent {
    profileActionService = inject(ProfileActionService);
    svgIconService = inject(SvgIconService);
    router = inject(Router)
    profile: InputSignal<ProfileModel> = input.required();

    sendMessageTrigger() {
        //Need to active the chat with this user
        this.router.navigate(['chat'])
    }
}
