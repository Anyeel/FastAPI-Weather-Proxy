import { Component, inject, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { WeatherService } from './core/services/weather.service';
import { Header } from './core/layout/header/header';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, Header],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  // Inject service
  protected weatherService = inject(WeatherService);
  protected readonly title = signal('frontend');
}
