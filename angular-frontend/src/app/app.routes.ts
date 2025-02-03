import { Routes } from '@angular/router';
import {HomeComponent} from "./components/home/home.component";
import {PageComponent} from "./components/page/page.component";
import {LoginComponent} from "./components/auth/login/login.component";
import {RegisterComponent} from "./components/auth/register/register.component";
import {SearchComponent} from "./components/search/search.component";
import {ProfileComponent} from "./components/profile/profile.component";

export const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'page/:name', component: PageComponent },
    { path: 'search', component: SearchComponent },
    { path: 'profile', component: ProfileComponent },
    { path: 'auth/login', component: LoginComponent },
    { path: 'auth/register', component: RegisterComponent },
    { path: '**', redirectTo: ''},
];
