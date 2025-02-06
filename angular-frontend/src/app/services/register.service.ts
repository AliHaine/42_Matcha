import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class RegisterService {

  INTERESTS: { [key: string]: string[] } = {
        "culture": [
            'Cinema',
            'Reading',
            'Writing',
            'Theater',
            'Painting',
            'Drawing',
            'Museum',
            'photography',
            'music',
        ],
        "sport": [
            'Bodybuilding',
            'Team-sport',
            'Extreme-sport',
            'Aqua-sport',
            'No-sport',
        ],
        "other": [
            'Animals',
            'Fashion',
            'Moto',
            'Collection',
            'Cooking',
            'Cleaning',
            'Video',
            'Esport',
        ]
    }

  constructor() { }
}
