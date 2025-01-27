import { Routes } from '@angular/router';
import {HomeComponent} from "./components/home/home.component";
import {PageComponent} from "./components/page/page.component";
import {LoginComponent} from "./components/auth/login/login.component";

export const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'page/:name', component: PageComponent },
    { path: 'auth/login', component: LoginComponent },
    { path: '**', redirectTo: ''},
];
