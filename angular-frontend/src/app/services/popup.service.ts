import {Injectable} from "@angular/core";

@Injectable({
    providedIn: 'root'
})
export class PopupService {
    message: string = "";
    classColor: string = ""; //green, blue or red
    private timeout: ReturnType<typeof setTimeout> | undefined;

    displayPopupBool(message: string, color: boolean): void {
        if (!this.popupInit(message))
            return;
        this.message = message;
        color ? this.classColor = "green": this.classColor = "red";
    }

    popupInit(message: string): boolean {
        if (!message) {
            this.resetPopup();
            return false;
        }
        this.runTask();
        return true;
    }

    runTask(): void {
        if (this.timeout !== undefined) {
            clearTimeout(this.timeout);
            this.timeout = undefined;
        }
        this.timeout = setTimeout(() => {
            this.resetPopup();
        }, 5000);
    }

    resetPopup(): void {
        clearTimeout(this.timeout);
        this.timeout = undefined;
        this.message = "";
        this.classColor = "";
    }
}