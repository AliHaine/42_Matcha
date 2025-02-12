import { Routes } from '@angular/router';
import {HomeComponent} from "./components/home/home.component";
import {PageComponent} from "./components/page/page.component";
import {LoginComponent} from "./components/auth/login/login.component";
import {RegisterComponent} from "./components/auth/register/register.component";
import {SearchComponent} from "./components/search/search.component";
import {ProfileComponent} from "./components/profile/profile.component";
import {authGuard} from "./others/auth.guard";
import {ChatComponent} from "./components/chat/chat.component";

export const routes: Routes = [
    { path: '', component: HomeComponent, canActivate: [authGuard] },
    { path: 'page/:name', component: PageComponent },
    { path: 'chat', component: ChatComponent, canActivate: [authGuard] },
    { path: 'search', component: SearchComponent, canActivate: [authGuard] },
    { path: 'profile', component: ProfileComponent, canActivate: [authGuard] },
    { path: 'profile/:id', component: ProfileComponent, canActivate: [authGuard] },
    { path: 'auth/login', component: LoginComponent },
    { path: 'auth/register', component: RegisterComponent },
    { path: '**', redirectTo: ''},
];
