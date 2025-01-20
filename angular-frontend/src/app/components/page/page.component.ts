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
    page: PageModel;

    constructor() {
        console.log("conmp constructor")
        const name = this.route.snapshot.paramMap.get("name")
        this.page = this.pageService.getPageWithKey(name);
    }
}
