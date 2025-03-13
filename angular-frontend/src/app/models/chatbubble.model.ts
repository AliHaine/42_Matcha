export class ChatBubbleModel {
    message: string;
    created_at: string;

    constructor(data: {[key: string]: string}) {
        this.message = data["message"];
        this.created_at = data["created_at"];

    }

}