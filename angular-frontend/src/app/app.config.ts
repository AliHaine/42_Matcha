import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import {provideRouter, RouteReuseStrategy} from '@angular/router';
import { provideHttpClient } from '@angular/common/http';

import { routes } from './app.routes';
import {HomeComponent} from "./components/home/home.component";

export const appConfig: ApplicationConfig = {
  providers: [provideZoneChangeDetection({ eventCoalescing: true }), provideRouter(routes), provideHttpClient(), { provide: RouteReuseStrategy, useClass: HomeComponent }]
};
