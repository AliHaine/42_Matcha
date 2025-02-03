import {inject, Injectable} from '@angular/core';
import {CardModel} from "../models/card.model";
import {InterestModel} from "../models/interest.model";
import {ApiService} from "./api.service";

@Injectable({
  providedIn: 'root'
})
export class CardService {

    apiService = inject(ApiService);
    private profiles: CardModel[] = [];
    private searchProfiles: CardModel[] = [];

    constructor() {


        this.profiles.push(new CardModel("Leila 24ans, Metz",
            "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus!" +
            " Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos" +
            " dicta est velit nemo..",
            [new InterestModel("/icons/interest.png", "Interest", ["Gaming", "Ecology", "Bodybuilding"]),
            new InterestModel("/icons/pharmacie.png", "Health", ["No smoker", "No alcohol", "Vegan"]),
            new InterestModel("/icons/body.png", "Body", ["Weight 58kg", "Size 166cm", "Sporty"]),
            new InterestModel("/icons/search.png", "Looking for", ["Friendly meeting", "Short-term commitment", "Casual contact"])],
            ""));

        this.profiles.push(new CardModel("Manon 18ans, Metz",
            "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus!" +
            " Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos" +
            " dicta est velit nemo..",
            [new InterestModel("/icons/interest.png", "Interest", ["Gaming", "Ecology", "Bodybuilding"]),
            new InterestModel("/icons/pharmacie.png", "Health", ["No smoker", "No alcohol", "Vegan"]),
            new InterestModel("/icons/body.png", "Body", ["Weight 58kg", "Size 166cm", "Sporty"]),
            new InterestModel("/icons/search.png", "Looking for", ["Friendly meeting", "Short-term commitment", "Casual contact"])],
            "https://i.pinimg.com/736x/21/f8/07/21f8077a1288fc475acf6d85dba83ffe.jpg"));

        this.profiles.push(new CardModel("Marie 28ans, Metz",
            "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus!" +
            " Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos" +
            " dicta est velit nemo..",
            [new InterestModel("/icons/interest.png", "Interest", ["Gaming", "Ecology", "Bodybuilding"]),
            new InterestModel("/icons/pharmacie.png", "Health", ["No smoker", "No alcohol", "Vegan"]),
            new InterestModel("/icons/body.png", "Body", ["Weight 58kg", "Size 166cm", "Sporty"]),
            new InterestModel("/icons/search.png", "Looking for", ["Friendly meeting", "Short-term commitment", "Casual contact"])],
            "https://img.wattpad.com/533a915c6bc0730244fd229e31e920937bbe8b38/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f77705077786868544c5f555936673d3d2d3237332e313439336635316662653138623462653433363938373839353537302e6a7067?s=fit&w=720&h=720"));

        this.profiles.push(new CardModel("Emily 38ans, Mulhouse",
            "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus!" +
            " Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos" +
            " dicta est velit nemo..",
            [new InterestModel("/icons/interest.png", "Interest", ["Gaming", "Ecology", "Bodybuilding"]),
            new InterestModel("/icons/pharmacie.png", "Health", ["No smoker", "No alcohol", "Vegan"]),
            new InterestModel("/icons/body.png", "Body", ["Weight 58kg", "Size 166cm", "Sporty"]),
            new InterestModel("/icons/search.png", "Looking for", ["Friendly meeting", "Short-term commitment", "Casual contact"])],
            "https://www.sciencesetavenir.fr/assets/img/2018/08/31/cover-r4x3w1200-5b8964e9c16e5-snapchat-dysmorphie-selfie.jpg"));

        this.profiles.push(new CardModel("Nathan 20ans, Mulhouse",
            "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus!" +
            " Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos" +
            " dicta est velit nemo..",
            [new InterestModel("/icons/interest.png", "Interest", ["Gaming", "Ecology", "Harassment"]),
            new InterestModel("/icons/pharmacie.png", "Health", ["No smoker", "No alcohol", "Vegan"]),
            new InterestModel("/icons/body.png", "Body", ["Weight 58kg", "Size 166cm", "Sporty"]),
            new InterestModel("/icons/search.png", "Looking for", ["Friendly meeting", "Short-term commitment", "Casual contact"])],
            "https://cdn.intra.42.fr/users/c3a0ea6cea763a36acd687089feb55ea/ngalzand.jpeg"));

        this.profiles.push(new CardModel("Leila 24ans, Metz",
            "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus!" +
            " Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos" +
            " dicta est velit nemo..",
            [new InterestModel("/icons/interest.png", "Interest", ["Gaming", "Ecology", "Bodybuilding"]),
            new InterestModel("/icons/pharmacie.png", "Health", ["No smoker", "No alcohol", "Vegan"]),
            new InterestModel("/icons/body.png", "Body", ["Weight 58kg", "Size 166cm", "Sporty"]),
            new InterestModel("/icons/search.png", "Looking for", ["Friendly meeting", "Short-term commitment", "Casual contact"])],
            "https://i.pinimg.com/originals/49/0f/2e/490f2edad1288b07eb1e973d4b58df0d.jpg"));

         this.profiles.push(new CardModel("Leila 24ans, Metz",
            "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus!" +
            " Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos" +
            " dicta est velit nemo..",
            [new InterestModel("/icons/interest.png", "Interest", ["Gaming", "Ecology", "Bodybuilding"]),
            new InterestModel("/icons/pharmacie.png", "Health", ["No smoker", "No alcohol", "Vegan"]),
            new InterestModel("/icons/body.png", "Body", ["Weight 58kg", "Size 166cm", "Sporty"]),
            new InterestModel("/icons/search.png", "Looking for", ["Friendly meeting", "Short-term commitment", "Casual contact"])],
            "https://i.pinimg.com/originals/49/0f/2e/490f2edad1288b07eb1e973d4b58df0d.jpg"));

        this.profiles.push(new CardModel("Leila 24ans, Metz",
            "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus!" +
            " Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos" +
            " dicta est velit nemo..",
            [new InterestModel("/icons/interest.png", "Interest", ["Gaming", "Ecology", "Bodybuilding"]),
            new InterestModel("/icons/pharmacie.png", "Health", ["No smoker", "No alcohol", "Vegan"]),
            new InterestModel("/icons/body.png", "Body", ["Weight 58kg", "Size 166cm", "Sporty"]),
            new InterestModel("/icons/search.png", "Looking for", ["Friendly meeting", "Short-term commitment", "Casual contact"])],
            "https://i.pinimg.com/originals/49/0f/2e/490f2edad1288b07eb1e973d4b58df0d.jpg"));

        this.searchProfiles = this.profiles.slice(0, this.profiles.length - 2);
      }

      getProfile(index: number): CardModel {
        return <CardModel>this.profiles.at(index);
      }

      refreshProfile() {
        console.log("sa")
          const salut = this.apiService.getProfilesFromBack()
        salut.subscribe((sub: any) => {
            for (const key in sub['matcha']) {
                console.log(sub['matcha'][key])
                const currentValue = sub['matcha'][key];
                this.profiles.push(new CardModel(currentValue['firstName'], "Metz", currentValue['description'], currentValue['']))
                console.log(sub['matcha'][key]);
            }
        })

        /*
          this.profiles.pop();

          this.profiles.push(new CardModel("NathanPiscineForm 18ans, Mulhouse",
            "Loorem ipsum dolor sit amet. Et facere fugiat ad vitae adipisci eos voluptatem illum et facere ducimus!" +
            " Non mollitia quis ut dignissimos dicta est velit nemo illum et facere ducimus! Non mollitia quis ut dignissimos" +
            " dicta est velit nemo..",
            [new InterestModel("/icons/interest.png", "Interest", ["Gaming", "Ecology", "Harassment"]),
            new InterestModel("/icons/pharmacie.png", "Health", ["No smoker", "No alcohol", "Vegan"]),
            new InterestModel("/icons/body.png", "Body", ["Weight 60kg", "Size 175cm", "Normale"]),
            new InterestModel("/icons/search.png", "Looking for", ["Friendly meeting", "Short-term commitment", "Casual contact"])],
            "https://cdn.intra.42.fr/users/c3a0ea6cea763a36acd687089feb55ea/ngalzand.jpeg"))

          console.log("refresh FUNCTION called")*/
      }

      getProfiles(): CardModel[] {
          return this.profiles;
      }

      getSearchProfiles(): CardModel[] {
        return this.searchProfiles;
      }
}