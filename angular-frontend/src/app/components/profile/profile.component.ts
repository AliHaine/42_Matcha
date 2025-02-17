import {Component, inject, OnInit, signal} from '@angular/core';
import {ProfileModel} from "../../models/profile.model";
import {ApiService} from "../../services/api.service";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-profile',
  imports: [],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css'
})
export class ProfileComponent implements OnInit {

  apiService = inject(ApiService);
  route = inject(ActivatedRoute);
  profile = signal<ProfileModel>(new ProfileModel({}));

  constructor() {
    this.apiService.getData('/profiles/14', {}).subscribe(result => {
      this.profile.set(new ProfileModel(result["user"]));
    });
  }

  ngOnInit(): void {
      console.log(this.route.paramMap);
    }
}
