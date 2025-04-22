import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";

interface Location {
  city: string;
  code: number;
}

@Injectable({
  providedIn: 'root'
})
export class LocationService {
  locations: Location[] = [];

  constructor(private http: HttpClient) { }

  cityGetFromGouv(city: string): Observable<any> {
      return this.http.get("https://geo.api.gouv.fr/communes/", { params: {"nom": city, "limit": 5, "boost": "population"} });
  }

  observableToSubscribe(observable: Observable <any>) {
      observable.subscribe(value => {
        if (value === null)
          return;
        this.cityGetFromGouv(value).subscribe(result => {
          this.locations = [];
          for (const name of result) {
            if (value === name['nom'])
              break;
            this.locations.push({ city: name['nom'], code: name['codeDepartement'] });
          }
        });
    });
  }
}
