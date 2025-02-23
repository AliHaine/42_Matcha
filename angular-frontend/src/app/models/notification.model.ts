export class NotificationModel {
    userId: number;
    userFullName: string;
    action: string;

    constructor(userId: number, userFullName: string, action: string) {
        this.userId = userId;
        this.userFullName = userFullName;
        this.action = action;
    }

}