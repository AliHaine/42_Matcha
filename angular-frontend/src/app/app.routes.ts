import { Routes } from '@angular/router';
import {HomeComponent} from "./components/home/home.component";
import {PageComponent} from "./components/page/page.component";

export const routes: Routes = [
    { path: '', component: HomeComponent, data: { reuse: true } },
    { path:'page/:name', component: PageComponent },
    { path: '**', redirectTo: ''}
];
