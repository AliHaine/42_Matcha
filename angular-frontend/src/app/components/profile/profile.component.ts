import {Component, inject, OnInit, signal} from '@angular/core';
import {ProfileModel} from "../../models/profile.model";
import {ApiService} from "../../services/api.service";
import {ActivatedRoute} from "@angular/router";
import {switchMap} from "rxjs";

@Component({
  selector: 'app-profile',
  imports: [],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css'
})
export class ProfileComponent implements OnInit {

  lorem: string = "Auxerunt haec vulgi sordidioris audaciam, quod cum ingravesceret penuria commeatuum, famis et furoris inpulsu Eubuli cuiusdam inter suos clari domum ambitiosam ignibus subditis inflammavit rectoremque ut sibi iudicio imperiali addictum calcibus incessens et pugnis conculcans seminecem laniatu miserando discerpsit. post cuius lacrimosum interitum in unius exitio quisque imaginem periculi sui considerans documento recenti similia formidabat.Post haec indumentum regale quaerebatur et ministris fucandae purpurae tortis confessisque pectoralem tuniculam sine manicis textam, Maras nomine quidam inductus est ut appellant Christiani diaconus, cuius prolatae litterae scriptae Graeco sermone ad Tyrii textrini praepositum celerari speciem perurgebant quam autem non indicabant denique etiam idem ad usque discrimen vitae vexatus nihil fateri conpulsus est. non indicabant denique etiam idem ad usque discrimen vitae vexatus nihil fateri conpulsus est. non indicabant denique etiam idem ad usque discrimen vitae vexatus nihil fateri conpulsus est."
  apiService = inject(ApiService);
  route = inject(ActivatedRoute);
  profile = signal<ProfileModel>(new ProfileModel({}));

  constructor() {
    const data = {
      "firstname": "Leila",
      "lastname": "Macron",
      "age": 19,
      "city": "Metz",
      "gender": "F",
      "description": this.lorem,
      "lookingFor": [],
      "shape": [],
      "health": [],
      "interests": [],
      "picturesNumber": 1,
      "status": "online",
    }
    this.profile.set(new ProfileModel(data));

    //this.profile.set(new ProfileModel(this.apiService.get());
  }

  ngOnInit(): void {
      console.log(this.route.paramMap);
    }
}
