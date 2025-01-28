import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class ApiService {
  private baseUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) { }

    getData(): Observable<any> {
      return this.http.get(`${this.baseUrl}/data`);
    }

    postData(targetUrl: string, dataToPost: any) {
      this.http.post(`${this.baseUrl}${targetUrl}`, dataToPost).subscribe(sub => {
        console.log(sub)
      });
    }

    getProfilesFromBack() {
      return this.http.get(`${this.baseUrl}/matcha`);
    }
}
