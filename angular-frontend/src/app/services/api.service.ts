import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {map, Observable, tap} from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class ApiService {
  private baseUrl = 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) { }

    getData(targetUrl: string, paramsToSend: any): Observable<any> {
      return this.http.get(`${this.baseUrl}${targetUrl}`, { params: paramsToSend });
    }

    postData(targetUrl: string, dataToPost: any): Observable<any> {
        return this.http.post(`${this.baseUrl}${targetUrl}`, dataToPost);
    }

    cityGetFromGouv(city: string) {
      this.http.get("https://geo.api.gouv.fr/communes/", { params: {"nom": city, "limit": 5, "boost": "population"} }).subscribe(response => {
          console.log(response)
      });
    }

    saveAccessToken(token: string) {
      localStorage.setItem('access_token', token);
    }

    getAccessToken(): string | null {
      return localStorage.getItem('access_token');
    }

    removeAccessToken() {
      localStorage.removeItem('access_token');
    }
}
