export class ChatModel {
    firstname: string;
    age: number;
    city: string;
    status: boolean;
    lastMsgTime: string;
    lastMessage: string;
    messages: string[] = [];

    constructor(data: {[key: string]: any}) {
        this.firstname = data['firstname'];
        this.age = data['age'];
        this.city = data['city'];
        this.status = data['status'];
        this.lastMsgTime = data['lastMsgTime'];
        this.lastMessage = data['lastMessage'];
    }
}