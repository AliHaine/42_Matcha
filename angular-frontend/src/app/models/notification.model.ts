export class NotificationModel {
    notifId: number;
    action: string;

    userFullName: string;
    profilePicture: string = 'defaultpp.jpg';
    userId: number;
    premium: boolean;

    constructor(notificationValues: {[key:string]: any}) {
        console.log(notificationValues);
        this.notifId = notificationValues["notif_id"];
        this.action = notificationValues["action"];

        this.userFullName = notificationValues["author"].fullname;
        //this.profilePicture = notificationValues["author"].avatar;
        this.userId = notificationValues["author"].id;
        this.premium = notificationValues["author"].premium;
    }

}