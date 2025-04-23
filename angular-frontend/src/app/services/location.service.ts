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
  locations: string[] = [];

  constructor(private http: HttpClient) { }

  cityGetFromGouv(city: string): Observable<any> {
      return this.http.get("https://geo.api.gouv.fr/communes/", { params: {"nom": city, "limit": 5, "boost": "population", "fields": "nom,codesPostaux"} });
  }

  observableToSubscribe(observable: Observable <any>) {
      observable.subscribe(value => {
        if (value === null)
          return;
        this.cityGetFromGouv(value).subscribe(result => {
          this.locations = [];
          for (const name of result) {
            const nameConverted = `${name['nom']} (${name['codesPostaux'][0]})`;
            if (value === nameConverted)
              break;
            this.locations.push(nameConverted);
          }
        });
    });
  }
}
