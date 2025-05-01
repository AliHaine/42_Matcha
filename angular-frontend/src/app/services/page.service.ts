import {inject, Injectable} from '@angular/core';
import {PageModel} from "../models/page.model";
import {HttpClient} from "@angular/common/http";
import {catchError, map, Observable, of} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class PageService {

    httpClient = inject(HttpClient)

    loadPage(pageName: string): Observable<PageModel> {
        let title = pageName.substring(pageName.indexOf("/")+1, pageName.lastIndexOf('.'));
        title = title.replaceAll('-', ' ').toUpperCase();
        return this.httpClient.get("/" + pageName, { responseType: 'text'}).pipe(
            map(data => new PageModel(title, data)),
            catchError(() => of(new PageModel("This page doesn't exist", "")))
        );
    }
}
