import {signal, WritableSignal} from "@angular/core";

export class NotificationModel {
    notifId: number;
    action: string;

    userFullName: string;
    profilePicturePath: WritableSignal<string>;
    havePicture: boolean;
    userId: number;
    premium: boolean;

    constructor(notificationValues: {[key:string]: any}) {
        this.notifId = notificationValues["notif_id"];
        this.action = notificationValues["action"];

        this.userFullName = notificationValues["author"].fullname;
        this.profilePicturePath = signal('defaultpp.jpg');
        this.havePicture = notificationValues["author"].avatar;
        this.userId = notificationValues["author"].id;
        this.premium = notificationValues["author"].premium;
    }

}