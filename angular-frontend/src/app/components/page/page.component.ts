import {Component, inject} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {PageModel} from "../../models/page.model";
import {PageService} from "../../services/page.service";

@Component({
  selector: 'app-page',
  imports: [],
  templateUrl: './page.component.html',
  styleUrl: './page.component.css'
})
export class PageComponent {

    private route = inject(ActivatedRoute);
    private pageService = inject(PageService);
    page: PageModel = new PageModel("Page not found", "The page you ask for don't exist");

    constructor() {
        const name = this.route.snapshot.paramMap.get("name")
        if (!name) {
            console.log("no page");
            return;
        }

        this.pageService.fillPageModel(this.page, name, "Conditions of use");
    }
}
