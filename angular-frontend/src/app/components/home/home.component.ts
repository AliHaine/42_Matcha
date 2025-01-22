import {Component, inject} from '@angular/core';
import {CardComponent} from "../card/card/card.component";
import {CardService} from "../../services/card.service";
import {NgForOf} from "@angular/common";
import {ActivatedRouteSnapshot, DetachedRouteHandle, RouteReuseStrategy} from "@angular/router";

@Component({
  selector: 'app-home',
  imports: [CardComponent, NgForOf],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements RouteReuseStrategy{
  cardService = inject(CardService);

  constructor() {
    console.log("called")
  }

  private cache = new Map<string, DetachedRouteHandle>();

  shouldDetach(route: ActivatedRouteSnapshot): boolean {
    return route.data?.['reuse'] ?? false;
  }

  store(route: ActivatedRouteSnapshot, handle: DetachedRouteHandle | null): void {
    if (handle) {
      this.cache.set(route.routeConfig?.path as string, handle);
    }
  }

  shouldAttach(route: ActivatedRouteSnapshot): boolean {
    return this.cache.has(route.routeConfig?.path as string);
  }

  retrieve(route: ActivatedRouteSnapshot): DetachedRouteHandle | null {
    return this.cache.get(route.routeConfig?.path as string) || null;
  }

  shouldReuseRoute(future: ActivatedRouteSnapshot, curr: ActivatedRouteSnapshot): boolean {
    return future.routeConfig === curr.routeConfig;
  }
}
