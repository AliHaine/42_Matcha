
# 42_Matcha: Angular 19 | Flask

Matcha is a complete dating website, with profiles, algo, searching, match, chat, and more. Demonstration (200K user in database): www.google.com. 
This is an educational project without financial or economic objective. The premium and Paypal systems are for demonstration and testing purposes only, there are no real payments or premium.

## Authors

- [Ali Yagmur](https://www.github.com/AliHaine) (Angular, Front-End)
- [Axel Kastler](https://www.github.com/ChromaXard) (Flask, Backend)


## Tech Stack

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) 
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Angular](https://img.shields.io/badge/angular-%23DD0031.svg?style=for-the-badge&logo=angular&logoColor=white)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)


## Features

- Login & registration system with multi-step forms
- Page manager for legal and informational pages (CGU, CGV, Rules, etc.)
- Matching system when two users like each other
- Smart matching algorithm based on interests, search filters, preferences, etc.
- Premium system that enhances the matching algorithm (demo only)
- Fully custom chat system for matched users
- Search page with advanced filters (age range, location, interests, etc.)
- Location autocomplete using Google Places API (France only)
PayPal sandbox integration for demo purposes


## Project Scale

- Over **200,000** user accounts generated for testing purposes
- Large dataset designed to simulate real-world load
- Useful for testing algorithm performance and scalability
- Optimized self-cache system to reduce loading time when browsing user profiles

## Dark pattern

⚠️ These dark patterns were implemented for educational demonstration only. Most are unethical or illegal and must never be used in real-world applications.

- Multi-step registration to increase user retention
- Nerfed algorithm depending on payment status and account age
- Location retrieval even when the user denies consent
- Excessive prompts to purchase premium features
- Infinite scroll for addictive content consumption
- Hard-to-read legal pages (CGU, rules, etc.)
- Hidden mandatory payments in the chat system


## Deployment

⚠️ Docker is required to run this project locally.

```
make dev      # Launch development environment
make prod     # Launch production environment
```



