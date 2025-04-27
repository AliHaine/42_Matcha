import { Injectable } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

@Injectable({
    providedIn: 'root',
})
export class SvgIconService {

    constructor(private matIconRegistry: MatIconRegistry, private domSanitizer: DomSanitizer) {
        this.registerIcons();
    }

    private registerIcons(): void {
        this.matIconRegistry.addSvgIcon(
            'home',
            this.domSanitizer.bypassSecurityTrustResourceUrl('icons/home.svg')
        );
        this.matIconRegistry.addSvgIcon(
            'search',
            this.domSanitizer.bypassSecurityTrustResourceUrl('icons/search.svg')
        );
        this.matIconRegistry.addSvgIcon(
            'chat',
            this.domSanitizer.bypassSecurityTrustResourceUrl('icons/chat.svg')
        );
        this.matIconRegistry.addSvgIcon(
            'notification',
            this.domSanitizer.bypassSecurityTrustResourceUrl('icons/notification.svg')
        );
        this.matIconRegistry.addSvgIcon(
            'profile',
            this.domSanitizer.bypassSecurityTrustResourceUrl('icons/profile.svg')
        );
        this.matIconRegistry.addSvgIcon(
            'logout',
            this.domSanitizer.bypassSecurityTrustResourceUrl('icons/logout.svg')
        );    }
}