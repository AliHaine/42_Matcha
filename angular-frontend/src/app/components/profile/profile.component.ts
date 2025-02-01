import {Component, inject, signal} from '@angular/core';
import {ProfileModel} from "../../models/profile.model";
import {ApiService} from "../../services/api.service";

@Component({
  selector: 'app-profile',
  imports: [],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css'
})
export class ProfileComponent {

  apiService = inject(ApiService);
  profile = signal<ProfileModel>(new ProfileModel({}));

  constructor() {
  }
}
