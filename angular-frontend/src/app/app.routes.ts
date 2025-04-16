import { Routes } from '@angular/router';
import {HomeComponent} from "./components/home/home.component";
import {PageComponent} from "./components/page/page.component";
import {LoginComponent} from "./components/auth/login/login.component";
import {RegisterComponent} from "./components/auth/register/register.component";
import {SearchComponent} from "./components/search/search.component";
import {ProfileComponent} from "./components/profile/profile.component";
import {authGuard} from "./others/auth.guard";
import {ChatComponent} from "./components/chat/chat.component";
import {loginGuard} from "./others/login.guard";
import {AccountComponent} from "./components/account/account.component";
import {EmailconfirmComponent} from "./components/emailconfirm/emailconfirm.component";
import { ForgotpassComponent } from './components/forgotpass/forgotpass.component';

export const routes: Routes = [
    { path: '', component: HomeComponent, canActivate: [authGuard] },
    { path: 'page/:name', component: PageComponent },
    { path: 'chat', component: ChatComponent, canActivate: [authGuard] },
    { path: 'search', component: SearchComponent, canActivate: [authGuard] },
    { path: 'account', component: AccountComponent, canActivate: [authGuard] },
    { path: 'profile/:id', component: ProfileComponent, canActivate: [authGuard] },
    { path: 'emailconfirm/:token', component: EmailconfirmComponent, canActivate: [authGuard] },
    { path: 'forgotpass/:token', component: ForgotpassComponent, canActivate: [loginGuard] },
    { path: 'auth', canActivate: [loginGuard], children: [{ path: 'register', component: RegisterComponent }, { path: 'login', component: LoginComponent }]},
    { path: '**', redirectTo: ''},
];
