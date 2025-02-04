import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable, tap} from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class ApiService {
  private baseUrl = 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) { }

    getData(): Observable<any> {
      return this.http.get(`${this.baseUrl}/data`);
    }

    postData(targetUrl: string, dataToPost: any) {
      this.http.post(`${this.baseUrl}${targetUrl}`, dataToPost, { 'headers': {'Authorization': `Bearer ${this.getAccessToken()}`}}).subscribe(sub => {
          console.log(sub);
      });
    }

    authentication(targetUrl: string, dataToPost: any) {
      this.http.post(`${this.baseUrl}${targetUrl}`, dataToPost).pipe(
          tap((sub: any) => {
            this.saveAccessToken(sub['access_token'])
          })
      ).subscribe()
    }

    getProfilesFromBack() {
      return this.http.get(`${this.baseUrl}/matcha`);
    }

    saveAccessToken(token: string) {
      localStorage.setItem('access_token', token);
    }

    removeAccessToken() {
      localStorage.removeItem('access_token');
    }

    getAccessToken(): string {
      const auth = localStorage.getItem('access_token');
      return auth ? auth : "null";
    }
}
