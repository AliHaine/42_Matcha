import {ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'app-loading',
  imports: [],
  templateUrl: './loading.component.html',
  styleUrl: './loading.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LoadingComponent {}
