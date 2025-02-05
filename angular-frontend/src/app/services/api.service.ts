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
      return this.http.get(`${this.baseUrl}${targetUrl}`, { params: paramsToSend, headers: {'Authorization': `Bearer ${this.getAccessToken()}`}});
    }

    postData(targetUrl: string, dataToPost: any): Observable<any> {
      if (this.getAccessToken() !== "null")
        return this.http.post(`${this.baseUrl}${targetUrl}`, dataToPost, {'headers': {'Authorization': `Bearer ${this.getAccessToken()}`}})
      else
        return this.http.post(`${this.baseUrl}${targetUrl}`, dataToPost)
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
