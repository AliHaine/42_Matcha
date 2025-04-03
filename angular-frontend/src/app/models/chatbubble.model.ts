export class ChatBubbleModel {
    author_id: number;
    message: string;
    type: string;
    created_at: string;

    constructor(data: {[key: string]: any}) {
        this.author_id = data["author_id"];
        this.message = data["message"];
        this.type = data["type"];
        this.created_at = data["created_at"];
    }
}