import {ChangeDetectionStrategy, Component, inject, OnInit, signal} from '@angular/core';
import {PageService} from "../../services/page.service";
import {ActivatedRoute} from "@angular/router";
import {PageModel} from "../../models/page.model";
import {switchMap} from 'rxjs'


@Component({
  selector: 'app-page',
  imports: [],
  templateUrl: './page.component.html',
  styleUrl: './page.component.css',
changeDetection: ChangeDetectionStrategy.OnPush
})
export class PageComponent implements OnInit {

    pageService = inject(PageService);
    route = inject(ActivatedRoute);
    page = signal<PageModel>(new PageModel("Loading", "Page is loading.."));

    ngOnInit() {
        this.route.paramMap.pipe(
            switchMap(param => {
                const fileName = "pages/" + param.get('name') + ".txt";
                return this.pageService.loadPage(fileName);
            })
        ).subscribe(page => {
            this.page.set(page);
        });
    }
}
