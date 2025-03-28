export class ChatModel {
    userId: number;
    firstname: string;
    age: number;
    city: string;
    status: boolean;
    lastMsgTime: string = "XX:XX";
    lastMessage: string = "Send your first message now.";

    constructor(data: {[key: string]: any}) {
        this.userId = data['id'];
        this.firstname = data['firstname'];
        this.age = data['age'];
        this.city = data['city'];
        this.status = data['status'];
        if (data['lastMessage']) {
            this.lastMsgTime = data["lastMessage"]["created_at"];
            this.lastMessage = data["lastMessage"]["message"];
        }
    }
}