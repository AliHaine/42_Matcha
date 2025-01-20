import {inject, Injectable} from '@angular/core';
import {PageModel} from "../models/page.model";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class PageService {

  pages = new Map<string, PageModel>();
  httpClient = inject(HttpClient)

  constructor() {
      this.httpClient.get("/conditions_of_use.txt", { responseType: "text" }).subscribe(
          (data) => {
            console.log(data)
            this.pages.set("name", new PageModel("test", data));
          },
          (error) => {
            console.error('Error loading the file', error);
          }
      );
  }

  fillPageModel(pageModel: PageModel, url: string, title: string) {
      this.httpClient.get("/conditions_of_use.txt", { responseType: "text" }).subscribe(
          (data) => {
            console.log(data)
            pageModel.title = title;
            pageModel.description = data;
          },
          (error) => {
            console.error('Error loading the file', error);
          }
      );
  }
}
