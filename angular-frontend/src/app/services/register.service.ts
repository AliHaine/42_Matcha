import {inject, Injectable, signal} from '@angular/core';
import {ApiService} from "./api.service";

@Injectable({
  providedIn: 'root'
})
export class RegisterService {

    apiService = inject(ApiService);
    private currentStep = signal<number>(1);
    INTERESTS = signal<{ [key: string]: string[] }>({});

    constructor() {
        this.apiService.getData("/getInformations/interests", {}).subscribe((data: any) => {
            this.INTERESTS.set(data["interests"]);
        });
    }

    setStep(step: number) {
        this.currentStep.set(step);
    }

    getStep() {
        return this.currentStep();
    }

    increaseStep() {
        this.setStep(this.currentStep() + 1);
    }
}
