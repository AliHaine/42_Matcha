import {Component, inject, input, OnInit} from '@angular/core';
import {PageService} from "../../services/page.service";
import {ActivatedRoute} from "@angular/router";
import {PageModel} from "../../models/page.model";

@Component({
  selector: 'app-page',
  imports: [],
  templateUrl: './page.component.html',
  styleUrl: './page.component.css'
})
export class PageComponent implements OnInit {

    pageService = inject(PageService);
    route = inject(ActivatedRoute);
    page: PageModel = new PageModel("Loading", "Page is loading..");

    ngOnInit() {
        this.route.paramMap.subscribe((param) => {
            const fileName = "pages/" + this.route.snapshot.paramMap.get('name') + ".txt"
            this.pageService.loadPage(fileName).subscribe(obs => {
                this.page = obs;
            });
        })
    }
}
