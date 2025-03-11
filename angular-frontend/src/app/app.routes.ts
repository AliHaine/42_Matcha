import { Routes } from '@angular/router';
import {HomeComponent} from "./components/home/home.component";
import {LoginComponent} from "./components/auth/login/login.component";
import {RegisterComponent} from "./components/auth/register/register.component";
import {ProfileComponent} from "./components/profile/profile.component";
import {authGuard} from "./others/auth.guard";
import {ChatComponent} from "./components/chat/chat.component";
import {loginGuard} from "./others/login.guard";

export const routes: Routes = [
    { path: '', component: HomeComponent, canActivate: [authGuard] },
    { path: 'chat', component: ChatComponent, canActivate: [authGuard] },
    { path: 'profile/:id', component: ProfileComponent, canActivate: [authGuard] },
    { path: 'auth', canActivate: [loginGuard], children: [{ path: 'register', component: RegisterComponent }, { path: 'login', component: LoginComponent }]},
    { path: '**', redirectTo: ''},
];
