import {inject, Injectable, signal} from '@angular/core';
import {ApiService} from "./api.service";
import {ProfileModel} from "../models/profile.model";

@Injectable({
  providedIn: 'root'
})
export class CardService {

    apiService = inject(ApiService);
    private profiles: ProfileModel[] = [];

    constructor() {

        this.apiService.getData("/matcha", {nb_profiles: 8}).subscribe(result => {
            for (const data of result["result"]) {
                this.profiles.push(new ProfileModel(data));
            }
        });
/*
        this.profiles.push(new CardModel({
            'firstname': "Enzo",
            'age': "17",
            'city': "Paris",
            'description': "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo..",
            "interests": ["Gaming", "Ecology", "Bodybuilding"],
            "health": ["No smoker", "No alcohol", "Vegan"],
            "shape": ["Weight 58kg", "Size 166cm", "Sporty"],
            "lookingFor": ["Friendly meeting", "Short-term commitment", "Casual contact"],
            'profilePicturePath': 'https://i.pinimg.com/originals/e5/1c/80/e51c80027ee944f8db032995fb37051c.jpg'
        }));

        this.profiles.push(new CardModel({
            'firstname': "Manon",
            'age': "18",
            'city': "Metz",
            'description': "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo..",
            "interests": ["Gaming", "Ecology", "Bodybuilding"],
            "health": ["No smoker", "No alcohol", "Vegan"],
            "shape": ["Weight 58kg", "Size 166cm", "Sporty"],
            "lookingFor": ["Friendly meeting", "Short-term commitment", "Casual contact"],
            'profilePicturePath': 'https://i.pinimg.com/736x/21/f8/07/21f8077a1288fc475acf6d85dba83ffe.jpg'
        }));

        this.profiles.push(new CardModel({
            'firstname': "Marie",
            'age': "28",
            'city': "Metz",
            'description': "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo..",
            "interests": ["Gaming", "Ecology", "Bodybuilding"],
            "health": ["No smoker", "No alcohol", "Vegan"],
            "shape": ["Weight 58kg", "Size 166cm", "Sporty"],
            "lookingFor": ["Friendly meeting", "Short-term commitment", "Casual contact"],
            'profilePicturePath': 'https://img.wattpad.com/533a915c6bc0730244fd229e31e920937bbe8b38/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f77705077786868544c5f555936673d3d2d3237332e313439336635316662653138623462653433363938373839353537302e6a7067?s=fit&w=720&h=720'
        }));

        this.profiles.push(new CardModel({
            'firstname': "Emily",
            'age': "38",
            'city': "Metz",
            'description': "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo..",
            "interests": ["Gaming", "Ecology", "Bodybuilding"],
            "health": ["No smoker", "No alcohol", "Vegan"],
            "shape": ["Weight 58kg", "Size 166cm", "Sporty"],
            "lookingFor": ["Friendly meeting", "Short-term commitment", "Casual contact"],
            'profilePicturePath': 'https://www.sciencesetavenir.fr/assets/img/2018/08/31/cover-r4x3w1200-5b8964e9c16e5-snapchat-dysmorphie-selfie.jpg'
        }));

        this.profiles.push(new CardModel({
            'firstname': "Nathan",
            'age': "20",
            'city': "Mulhouse",
            'description': "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo..",
            "interests": ["Gaming", "Ecology", "Bodybuilding"],
            "health": ["No smoker", "No alcohol", "Vegan"],
            "shape": ["Weight 58kg", "Size 166cm", "Sporty"],
            "lookingFor": ["Friendly meeting", "Short-term commitment", "Casual contact"],
            'profilePicturePath': 'https://cdn.intra.42.fr/users/c3a0ea6cea763a36acd687089feb55ea/ngalzand.jpeg'
        }));

        this.profiles.push(new CardModel({
            'firstname': "Leila",
            'age': "24",
            'city': "Mulhouse",
            'description': "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo..",
            "interests": ["Gaming", "Ecology", "Bodybuilding"],
            "health": ["No smoker", "No alcohol", "Vegan"],
            "shape": ["Weight 58kg", "Size 166cm", "Sporty"],
            "lookingFor": ["Friendly meeting", "Short-term commitment", "Casual contact"],
            'profilePicturePath': 'https://i.pinimg.com/originals/49/0f/2e/490f2edad1288b07eb1e973d4b58df0d.jpg'
        }));

        this.profiles.push(new CardModel({
            'firstname': "Jerome",
            'age': "30",
            'city': "Mulhouse",
            'description': "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo..",
            "interests": ["Gaming", "Ecology", "Bodybuilding"],
            "health": ["No smoker", "No alcohol", "Vegan"],
            "shape": ["Weight 58kg", "Size 166cm", "Sporty"],
            "lookingFor": ["Friendly meeting", "Short-term commitment", "Casual contact"],
            'profilePicturePath': 'https://cdn.intra.42.fr/users/c150436de6d3e0978aa71fa2c4eb04f4/jmathieu.jpeg'
        }));

        this.profiles.push(new CardModel({
            'firstname': "Marie-jeanne",
            'age': "42",
            'city': "Saint-goerge les ails",
            'description': "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos dicta est velit nemo..",
            "interests": ["Gaming", "Ecology", "Bodybuilding"],
            "health": ["No smoker", "No alcohol", "Vegan"],
            "shape": ["Weight 58kg", "Size 166cm", "Sporty"],
            "lookingFor": ["Friendly meeting", "Short-term commitment", "Casual contact"],
            'profilePicturePath': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ7iSFR6QIn17S_j89EPHXhfRZmv3FS3OuUzQ&s'
        }));*/

      }

      refreshProfile() {
        this.profiles = [];
          this.apiService.getData("/matcha", {nb_profiles: 8}).subscribe(result => {
              for (const data of result["result"]) {
                  this.profiles.push(new ProfileModel(data));
              }
          });
      }

      getProfiles(): ProfileModel[] {
          return this.profiles;
      }
}