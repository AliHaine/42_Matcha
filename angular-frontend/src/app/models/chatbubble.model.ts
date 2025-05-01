import {signal, WritableSignal} from "@angular/core";

export class ChatBubbleModel {
    author_id: number;
    content: WritableSignal<string> = signal("");
    src: string = "";
    type: string;
    created_at: string;

    constructor(data: {[key: string]: any}) {
        this.author_id = data["author_id"];
        this.type = data["type"];
        //if the type is image, the content will be load in the BubbleFactory (to load the image with a http request)
        if (this.type === "image")
            this.src = data["message"];
        else
            this.content.set(data["message"]);
        this.created_at = data["created_at"];
    }
}