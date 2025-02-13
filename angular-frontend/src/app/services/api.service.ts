import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {map, Observable, tap} from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class ApiService {
  private baseUrl = 'http://10.13.1.10:5000/api';

  constructor(private http: HttpClient) { }

    getData(targetUrl: string, paramsToSend: any): Observable<any> {
      return this.http.get(`${this.baseUrl}${targetUrl}`, { params: paramsToSend });
    }

    postData(targetUrl: string, dataToPost: any): Observable<any> {
        return this.http.post(`${this.baseUrl}${targetUrl}`, dataToPost);
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
