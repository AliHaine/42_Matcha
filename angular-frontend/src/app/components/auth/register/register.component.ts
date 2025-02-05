import {Component, inject} from '@angular/core';
import {
    AbstractControl,
    FormControl,
    FormGroup,
    ReactiveFormsModule,
    ValidationErrors,
    ValidatorFn,
    Validators
} from "@angular/forms";
import {Router, RouterLink} from "@angular/router";
import {ApiService} from "../../../services/api.service";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-register',
    imports: [ReactiveFormsModule, RouterLink, NgIf],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {

    currentStep: number = 3;
    apiService = inject(ApiService);
    router = inject(Router)

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

    formControlGroupStep3 = new FormGroup({
        artCulture: new FormControl('', Validators.required),
        sportActivity: new FormControl('', Validators.required),
        other: new FormControl('', Validators.required),
        description: new FormControl('', Validators.required),
    });

    submit(event: Event, values: any) {
      event.preventDefault();
      values['step'] = this.currentStep;
      console.log(values);
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
