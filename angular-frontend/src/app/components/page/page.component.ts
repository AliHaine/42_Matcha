import {ChangeDetectionStrategy, Component, inject, OnInit, signal} from '@angular/core';
import {PageService} from "../../services/page.service";
import {ActivatedRoute, Router} from "@angular/router";
import {PageModel} from "../../models/page.model";
import {mergeMap, switchMap} from 'rxjs'
import { ApiService } from '../../services/api.service';
import { PopupService } from '../../services/popup.service';

@Component({
  selector: 'app-page',
  imports: [],
  templateUrl: './page.component.html',
  styleUrl: './page.component.css',
changeDetection: ChangeDetectionStrategy.OnPush
})
export class PageComponent implements OnInit {

    pageService = inject(PageService);
    apiService = inject(ApiService);
    popupService = inject(PopupService);
    route = inject(ActivatedRoute);
    router = inject(Router);
    page = signal<PageModel>(new PageModel("Loading", "Page is loading.."));

    ngOnInit() {
        this.route.paramMap.pipe(
            mergeMap(param => this.apiService.getData(`/pages/${param.get('name')}`, {}))
        ).subscribe(pageResult => {
            if (!pageResult['success']) {
                this.router.navigate(['/']);
                this.popupService.displayPopupBool(pageResult['message'], pageResult['success']);
                return;
            }
            this.page.set(new PageModel(pageResult['title'], pageResult['content']));
        });
    }
}
