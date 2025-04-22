import {Injectable} from "@angular/core";

@Injectable({
    providedIn: 'root'
})
export class PopupService {
    message: string = "";
    classColor: string = ""; //green, blue or red

    displayPopup(message: string, color: string): void {
        if (!message) {
            this.resetPopup();
            return;
        }
        this.message = message;
        this.classColor = color;
    }

    displayPopupBool(message: string, color: boolean): void {
        if (!message) {
            this.resetPopup();
            return;
        }
        this.message = message;
        color ? this.classColor = "green": this.classColor = "red";
    }

    resetPopup(): void {
        this.message = "";
        this.classColor = "";
    }
}