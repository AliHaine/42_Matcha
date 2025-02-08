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
            console.log("Before " + JSON.stringify(this.INTERESTS()));
            console.log(typeof data["interests"])
            console.log(data["interests"])
            this.INTERESTS.set(data["interests"]);
            console.log(data["interests"])
            console.log(this.INTERESTS())
            console.log("After " + this.INTERESTS()['Culture']);
        });
    }
}
