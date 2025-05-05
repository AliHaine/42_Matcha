import {inject, Injectable} from "@angular/core";
import {ApiService} from "../services/api.service";
import {NotificationModel} from "../models/notification.model";


@Injectable({
    providedIn: 'root',
})
export class NotificationFactory {
    apiService = inject(ApiService);

    getNewNotification(data: {[key: string]: any}): NotificationModel {
        const notificationModel = new NotificationModel(data);
        if (!notificationModel.havePicture)
            return notificationModel;
        this.apiService.getDataImg("/profiles/profile_pictures", {"user_id": notificationModel.userId, "photo_number": 0}).subscribe(result => {
            const reader = new FileReader();
            reader.readAsDataURL(result);
            reader.onloadend = () => {
                notificationModel.profilePicturePath.set(reader.result as string);
            }
        });
        return notificationModel;
    }
}