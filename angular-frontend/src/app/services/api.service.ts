import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {catchError, map, Observable, of, switchMap, throwError} from 'rxjs';
import {backendIP} from "../app.config";

@Injectable({
  providedIn: 'root'
})

export class ApiService {
  private baseUrl = `http://${backendIP}/api`;
  isButtonLoading: boolean = false;

  constructor(private http: HttpClient) { }

    getData(targetUrl: string, paramsToSend: any): Observable<any> {
        return this.http.get(`${this.baseUrl}${targetUrl}`, { params: paramsToSend })
            .pipe(
                catchError(error => {
                  return of(null);
                })
            );
    }

    getDataImg(targetUrl: string, paramsToSend: any): Observable<any> {
        return this.http.get(`${this.baseUrl}${targetUrl}`, { params: paramsToSend, responseType: "blob" }).pipe(
          catchError(error => {
            return of(null);
          })
      );
    }

    postData(targetUrl: string, dataToPost: any): Observable<any> {
        return this.http.post(`${this.baseUrl}${targetUrl}`, dataToPost)
          .pipe(
            catchError(error => {
              return of(null);
            })
          );
    }

    putData(targetUrl: string, dataToPost: any): Observable<any> {
      return this.http.put(`${this.baseUrl}${targetUrl}`, dataToPost).pipe(
        catchError(error => {
            return of(null);
        })
    );
    }

    deleteData(targetUrl: string, paramsToSend: any): Observable<any> {
      return this.http.delete(`${this.baseUrl}${targetUrl}`, { params: paramsToSend }).pipe(
        catchError(error => {
          return of(null);
        })
    );
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

    getClientIp(): Observable<string> {
        return this.http.get("https://checkip.amazonaws.com/", {responseType: "text"}).pipe(
          catchError(_ => {
            return "Mulhouse (68100)";
          })
        );
    }

    getClientCityFromIp(): Observable<string> {
      return this.getClientIp().pipe(
          switchMap(ipAddress => this.http.get<any>("http://ip-api.com/json/" + ipAddress).pipe(
              catchError(_ => {
                return of({ city: "Mulhouse", zip: '68100' })
              })
          )),
          map(value => `${value.city} (${value.zip.slice(0,5)})`),
          catchError(_ => {
            return "Mulhouse (68100)";
          })
      )
    }
}
