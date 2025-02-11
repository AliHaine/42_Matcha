import {Component, effect, inject, signal} from '@angular/core';
import {
    AbstractControl, FormArray,
    FormControl,
    FormGroup,
    ReactiveFormsModule,
    ValidationErrors,
    ValidatorFn,
    Validators
} from "@angular/forms";
import {Router, RouterLink} from "@angular/router";
import {ApiService} from "../../../services/api.service";
import {NgForOf, NgIf} from "@angular/common";
import {RegisterService} from "../../../services/register.service";
import {AuthService} from "../../../services/auth.service";

@Component({
    selector: 'app-register',
    imports: [ReactiveFormsModule, RouterLink, NgIf, NgForOf],
    templateUrl: './register.component.html',
    styleUrl: './register.component.css'
})

export class RegisterComponent {

    currentStep: number = 1;
    apiService = inject(ApiService);
    router = inject(Router)
    registerService = inject(RegisterService);

    formControlGroupStep1 = new FormGroup({
        lastname: new FormControl('tes', Validators.required),
        firstname: new FormControl('test', Validators.required),
        email: new FormControl('test@gmail.com', [Validators.required, Validators.email]),
        password: new FormControl('Test123-', Validators.required),
        passwordConfirm: new FormControl('Test123-', Validators.required),
        age: new FormControl(19, [Validators.required, Validators.min(15), Validators.max(80)]),
        gender: new FormControl('M', Validators.required)
    }, { validators: passwordValidator });

    formControlGroupStep2 = new FormGroup({
        city: new FormControl('', Validators.required),
        searching: new FormControl('', Validators.required),
        commitment: new FormControl('', Validators.required),
        frequency: new FormControl('', Validators.required),

        weight: new FormControl('', Validators.required),
        size: new FormControl('', Validators.required),
        shape: new FormControl('', Validators.required),

        smoking: new FormControl('', Validators.required),
        alcohol: new FormControl('', Validators.required),
        diet: new FormControl('', Validators.required),
    });

    formControlGroupStep3: FormGroup = new FormGroup({
        // Interests forms are automatically generated in the constructor
        description: new FormControl('', Validators.required),
    } as { [key:string]: any });

    constructor() {
        effect(() => {
            for (const key in this.registerService.INTERESTS()) {
                this.formControlGroupStep3.addControl(key, new FormArray([]));
                const currentController = this.formControlGroupStep3.get(key) as FormArray;
                this.registerService.INTERESTS()[key].forEach(() => {
                    currentController.push(new FormControl(false));
                });
            }
        });
    }

    submit(event: Event, values: any) {
      event.preventDefault();
      values['step'] = this.currentStep;

      if (this.currentStep === 3)
          this.setupInterests(values);

      this.apiService.postData('/auth/register', values).subscribe(response => {
          if (!response['success']) {
              console.log("Error from back " + response)
              return;
          }
          if (this.currentStep === 1)
              this.apiService.saveAccessToken(response['access_token'])
          if (this.currentStep === 3)
            this.router.navigate([''])
          this.currentStep++
      });
    }

    getFromArray(name: string): FormArray {
        return this.formControlGroupStep3.get(name) as FormArray;
    }

    getGroupForm3(): string[] {
        return Object.keys(this.formControlGroupStep3.controls).filter((key) => key != "description");
    }

    setupInterests(values: any) {
        for (const key in values) {
              const index: string[] = [];
              if (key === "description" || key == "step")
                  continue;
              for (let i = 0; i < values[key].length; i++) {
              if (values[key].at(i) === true)
                  index.push(<string>this.registerService.INTERESTS()[key].at(i));
            }
            values[key] = index;
        }
    }
}

export const passwordValidator: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
    const password: string = <string>control.get('password')?.value;
    if (password.length < 8 || !/[A-Z]/.test(password) || !/[a-z]/.test(password) || !/[1-9]/.test(password))
        return {"securityError": true};

    if (password !== <string>control.get('passwordConfirm')?.value) {
        return {"confirmationError": true};
    }

    return null;
};
