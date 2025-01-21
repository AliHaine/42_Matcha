import {inject, Injectable} from '@angular/core';
import {PageModel} from "../models/page.model";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class PageService {

    httpClient = inject(HttpClient)
    page = new PageModel("Loading", "Page is loading..");

    constructor() {
        console.log("constructor service")
    }

    loadPage(pageName: string) {
        let title = pageName.substring(pageName.indexOf("/")+1, pageName.lastIndexOf('.'));
        title = title.replaceAll('-', ' ').toUpperCase();
        this.httpClient.get("/" + pageName, { responseType: 'text'}).subscribe(
            (data) => {
                this.page = new PageModel(title, data);
             },
            (error) => {
                this.page = new PageModel("Page not found", "This page don't exist..");
            })
    }
}
