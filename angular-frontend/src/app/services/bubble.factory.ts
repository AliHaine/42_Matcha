import {inject, Injectable} from "@angular/core";
import {ApiService} from "./api.service";
import { ChatBubbleModel } from "../models/chatbubble.model";

@Injectable({
    providedIn: 'root'
})
export class BubbleFactory {
    apiService = inject(ApiService);

    getNewBubble(data: {[key: string]: any}): ChatBubbleModel {
        const bubbleModel = new ChatBubbleModel(data);
        if (bubbleModel.type !== "image")
            return bubbleModel;
        this.apiService.getDataImg("/chat/recover_image", {"image_name": bubbleModel.src}).subscribe(result => {
            const reader = new FileReader();
            reader.readAsDataURL(result);
            reader.onloadend = () => {
                bubbleModel.content.set(reader.result as string);
            }
        });
        return bubbleModel;
    }
}
