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
        );
        this.matIconRegistry.addSvgIcon(
            'target',
            this.domSanitizer.bypassSecurityTrustResourceUrl('icons/target.svg')
        );
        this.matIconRegistry.addSvgIcon(
            'heart',
            this.domSanitizer.bypassSecurityTrustResourceUrl('icons/heart.svg')
        );
        this.matIconRegistry.addSvgIcon(
            'star',
            this.domSanitizer.bypassSecurityTrustResourceUrl('icons/star.svg')
        );
        this.matIconRegistry.addSvgIcon(
            'x',
            this.domSanitizer.bypassSecurityTrustResourceUrl('icons/x.svg')
        );
        this.matIconRegistry.addSvgIcon(
            'report',
            this.domSanitizer.bypassSecurityTrustResourceUrl('icons/report.svg')
        );
        this.matIconRegistry.addSvgIcon(
            'premium',
            this.domSanitizer.bypassSecurityTrustResourceUrl('icons/premium.svg')
        );
        this.matIconRegistry.addSvgIcon(
            'folder',
            this.domSanitizer.bypassSecurityTrustResourceUrl('icons/folder.svg')
        );
        this.matIconRegistry.addSvgIcon(
            'send',
            this.domSanitizer.bypassSecurityTrustResourceUrl('icons/send.svg')
        );
        this.matIconRegistry.addSvgIcon(
            'arrow',
            this.domSanitizer.bypassSecurityTrustResourceUrl('icons/arrow.svg')
        );
    }
}