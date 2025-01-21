import {Component, inject, OnInit} from '@angular/core';
import {PageService} from "../../services/page.service";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-page',
  imports: [],
  templateUrl: './page.component.html',
  styleUrl: './page.component.css'
})
export class PageComponent implements OnInit {

    pageService = inject(PageService);
    route = inject(ActivatedRoute);

    ngOnInit() {
        this.route.paramMap.subscribe((param) => {
            const fileName = "pages/" + this.route.snapshot.paramMap.get('name') + ".txt"
            this.pageService.loadPage(fileName);
        })
    }
}
