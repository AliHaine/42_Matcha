import { Component, effect, inject, signal } from "@angular/core";
import {
	FormArray,
	FormControl,
	FormGroup,
	ReactiveFormsModule,
	Validators,
} from "@angular/forms";
import { Router, RouterLink } from "@angular/router";
import { ApiService } from "../../../services/api.service";
import { RegisterService } from "../../../services/register.service";
import { AuthService } from "../../../services/auth.service";
import { TextFieldModule } from "@angular/cdk/text-field";
import { MatFormField } from "@angular/material/form-field";
import { MatInput } from "@angular/material/input";
import { LocationComponent } from "../../utils/location/location.component";
import { PopupService } from "../../../services/popup.service";
import {ButtonComponent} from "../../utils/button/button.component";

@Component({
	selector: "app-register",
	imports: [
		ReactiveFormsModule,
		RouterLink,
		TextFieldModule,
		MatFormField,
		MatInput,
		LocationComponent,
		ButtonComponent,
	],
	templateUrl: "./register.component.html",
	styleUrl: "./register.component.css",
})
export class RegisterComponent {
	apiService = inject(ApiService);
	router = inject(Router);
	registerService = inject(RegisterService);
	authService = inject(AuthService);
	popupService = inject(PopupService);
	isCityGet = signal(0);

	formControlGroupStep1 = new FormGroup(
		{
			lastname: new FormControl("", Validators.required),
			firstname: new FormControl("", Validators.required),
			email: new FormControl("", [
				Validators.required,
				Validators.email,
			]),
			username: new FormControl("", Validators.required),
			password: new FormControl("", Validators.required),
			passwordConfirm: new FormControl("", Validators.required),
			age: new FormControl('', [
				Validators.required,
				Validators.min(15),
				Validators.max(80),
			]),
			hetero: new FormControl(true, Validators.required),
			gender: new FormControl("M", Validators.required),
		}
	);

	formControlGroupStep2 = new FormGroup({
		city: new FormControl("", Validators.required),
		searching: new FormControl("", Validators.required),
		commitment: new FormControl("", Validators.required),
		frequency: new FormControl("", Validators.required),

		weight: new FormControl("", Validators.required),
		size: new FormControl("", Validators.required),
		shape: new FormControl("", Validators.required),

		smoking: new FormControl("", Validators.required),
		alcohol: new FormControl("", Validators.required),
		diet: new FormControl("", Validators.required),
	});

	formControlGroupStep3: FormGroup = new FormGroup({
		// Interests forms are automatically generated in the constructor
		description: new FormControl("", Validators.required),
	} as { [key: string]: any });

	constructor() {
		effect(() => {
			for (const key in this.registerService.INTERESTS()) {
				this.formControlGroupStep3.addControl(key, new FormArray([]));
				const currentController = this.formControlGroupStep3.get(
					key
				) as FormArray;
				this.registerService.INTERESTS()[key].forEach(() => {
					currentController.push(new FormControl(false));
				});
			}
		});

		this.getLocationFromIp();
	}

	submit(event: Event, values: any) {
		event.preventDefault();
		values["step"] = this.registerService.currentStep();

		if (this.registerService.currentStep() === 3) this.setupInterests(values);

		this.apiService.postData("/auth/register", values).subscribe((response) => {
			this.apiService.isButtonLoading = false;
			this.popupService.displayPopupBool(
				response["message"],
				response["success"]
			);
			if (!response["success"]) return;
			if (this.registerService.currentStep() === 1) {
				this.router.navigate(["auth/login"]);
				return;
			}
			if (this.registerService.currentStep() === 3) {
				this.authService.login();
				this.router.navigate([""]);
				this.registerService.setStep(1);
			}
			this.registerService.increaseStep();
		});
	}

	getFromArray(name: string): FormArray {
		return this.formControlGroupStep3.get(name) as FormArray;
	}

	getGroupForm3(): string[] {
		return Object.keys(this.formControlGroupStep3.controls).filter(
			(key) => key != "description"
		);
	}

	setupInterests(values: any) {
		for (const key in values) {
			const index: string[] = [];
			if (key === "description" || key == "step") continue;
			for (let i = 0; i < values[key].length; i++) {
				if (values[key].at(i) === true)
					index.push(<string>this.registerService.INTERESTS()[key].at(i));
			}
			values[key] = index;
		}
	}

	getLocationFromIp() {
		this.apiService.getClientCityFromIp().subscribe((city) => {
			this.formControlGroupStep2.controls.city.setValue(city);
		});
	}
}