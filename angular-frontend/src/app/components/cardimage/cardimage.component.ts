import {Component, inject, input, InputSignal, signal} from '@angular/core';
import {ProfileModel} from "../../models/profile.model";
import {ProfileActionService} from "../../services/profileaction.service";
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
    router = inject(Router)
    profile: InputSignal<ProfileModel> = input.required();
    currentIndex = signal<number>(0);

    sendMessageTrigger() {
        //Need to active the chat with this user
        this.router.navigate(['chat'])
    }

    arrowLeftClick() {
        this.currentIndex.set(this.currentIndex()-1);
        if (this.currentIndex() < 0)
            this.currentIndex.set(this.profile().profilePicturePath().length-1);
    }

    arrowRightClick() {
        this.currentIndex.set(this.currentIndex()+1);
        if (this.currentIndex() > this.profile().profilePicturePath().length-1)
            this.currentIndex.set(0);
    }
}
