export class ChatModel {
    userId: number;
    firstname: string;
    age: number;
    city: string;
    status: boolean;
    lastMsgTime: string;
    lastMessage: string;
    messages: string[] = [];

    constructor(data: {[key: string]: any}) {
        this.userId = data['id'];
        this.firstname = data['firstname'];
        this.age = data['age'];
        this.city = data['city'];
        this.status = data['status'];
        if (!data['lastMsgTime'])
        {
            this.lastMsgTime = "00:00";
            this.lastMessage = "Send your first message now.";
        } else {
            this.lastMsgTime = data['lastMsgTime'];
            this.lastMessage = data['lastMessage'];
        }
    }
}