import {inject, Injectable, OnInit} from '@angular/core';
import {PageModel} from "../models/page.model";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class PageService implements OnInit {

  pages = new Map<string, PageModel>();
  httpClient = inject(HttpClient)

   constructor() {
      console.log("constructor")
   }

  ngOnInit() {
      console.log("oninit")
      this.loadPages().then(() => {
          console.log("full");
      })
  }

  async loadPages() {
      const pageToRequests = [
          this.createPage("not-found", "Page not found", "/pages/not_found.txt"),
          this.createPage("conditions-use", "Conditions of use", "/pages/conditions_of_use.txt"),
          this.createPage("rules", "Rules", "/pages/conditions_of_use.txt")
      ];
      await Promise.all(pageToRequests);
  }

  createPage(pageKey: string, pageName: string, pageContentUrl: string) {
      return this.httpClient.get(pageContentUrl, { responseType: "text" }).subscribe(
          (data) => {
            this.pages.set(pageKey, new PageModel(pageName, data));
            console.log("test")
          },
          (error) => {
            console.error('Error loading the file', error);
          }
      );
  }

  getPageWithKey(pageKey: string): PageModel {
      return this.pages.has(pageKey) ? <PageModel>this.pages.get(pageKey) : <PageModel>this.pages.get("not-found");
  }
}
