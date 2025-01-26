import {inject, Injectable} from '@angular/core';
import {PageModel} from "../models/page.model";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class PageService {

    httpClient = inject(HttpClient)
    page = new PageModel("Loading", "Page is loading..");

    constructor() {
        console.log("constructor service")
    }

    loadPage(pageName: string): Observable<PageModel> {
        let title = pageName.substring(pageName.indexOf("/")+1, pageName.lastIndexOf('.'));
        title = title.replaceAll('-', ' ').toUpperCase();
        return new Observable(obs => {
            this.httpClient.get("/" + pageName, { responseType: 'text'}).subscribe(
            (data) => {
                obs.next(new PageModel(title, data))
             },error => {
                obs.next(new PageModel("This page doesn't exist", ""));
            })
        })
    }
}
