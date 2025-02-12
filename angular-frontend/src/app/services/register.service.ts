import {inject, Injectable, signal} from '@angular/core';
import {ApiService} from "./api.service";

@Injectable({
  providedIn: 'root'
})
export class RegisterService {

    apiService = inject(ApiService);
    INTERESTS = signal<{ [key: string]: string[] }>({});

    constructor() {
        this.apiService.getData("/getInformations/interests", {}).subscribe((data: any) => {
            this.INTERESTS.set(data["interests"]);
        });
    }
}
