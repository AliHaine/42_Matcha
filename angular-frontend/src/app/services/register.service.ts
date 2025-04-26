import {inject, Injectable, signal} from '@angular/core';
import {ApiService} from "./api.service";

@Injectable({
  providedIn: 'root'
})
export class RegisterService {

    apiService = inject(ApiService);
    currentStep = signal<number>(3);
    INTERESTS = signal<{ [key: string]: string[] }>({});
    registerInfo = signal<{ [key: string]: string[] }>({});

    constructor() {
        this.apiService.getData("/getInformations/interests", {}).subscribe((data: any) => {
            this.INTERESTS.set(data["interests"]);
        });
        this.apiService.getData("/getInformations/register", {}).subscribe((data: any) => {
            this.registerInfo.set(data["registerInfo"]);
        });
    }

    setStep(step: number) {
        this.currentStep.set(step);
    }

    increaseStep() {
        this.setStep(this.currentStep() + 1);
    }
}
