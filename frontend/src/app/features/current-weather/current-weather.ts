import { Component, inject } from '@angular/core';
import { AsyncPipe, DecimalPipe } from '@angular/common';
import { ActivatedRoute } from '@angular/router';

import { MatCard, MatCardContent, MatCardHeader, MatCardTitle } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinner } from '@angular/material/progress-spinner';

import { WeatherService } from '../../core/services/weather.service';
import { map, Observable, of, switchMap } from 'rxjs';
import { WeatherResponse } from '../../core/models/weather.model';
import { MatDivider } from '@angular/material/list';

/**
 * Component responsible for displaying current weather conditions
 * for one or multiple cities.
 */
@Component({
  selector: 'app-current-weather',
  standalone: true,
  imports: [
    AsyncPipe,
    MatProgressSpinner,
    MatCard,
    MatIconModule,
    MatCardHeader,
    MatCardTitle,
    MatCardContent,
    DecimalPipe,
    MatDivider,
  ],
  templateUrl: './current-weather.html',
  styleUrl: './current-weather.scss',
})
export class CurrentWeather {
  private route = inject(ActivatedRoute);
  protected weatherService = inject(WeatherService);

  /**
   * Dictionary mapping raw API descriptions to branded UI strings
   */
  private weatherTranslations: { [key: string]: string } = {
    'clear sky': 'Bright & Sunny',
    mist: 'Morning Haze',
    smoke: 'Hazy Skies',
    haze: 'Hazy View',
    dust: 'Dusty Air',
    fog: 'Foggy Conditions',
    sand: 'Sandstorm',
    ash: 'Volcanic Ash',
    squall: 'Sudden Squalls',
    tornado: 'Tornado Warning',
    'overcast clouds': 'Cloudy & Grey',
    'broken clouds': 'Partly Cloudy',
    'scattered clouds': 'Light Clouds',
    'few clouds': 'Mostly Sunny',
  };

  /**
   * Reactive pipeline that reads city IDs from the URL and fetches current weather.
   */
  public weatherData$: Observable<WeatherResponse[]> = this.route.queryParams.pipe(
    map((params) => params['cities']),
    switchMap((citiesParam) => {
      if (!citiesParam) return of([]);

      // Convert the URL string into an array of numbers
      const cityIds = citiesParam.split(',').map((id: string) => +id);

      if (cityIds.length === 1) {
        // Single City
        return this.weatherService.getSingleWeather(cityIds[0]).pipe(map((response) => [response]));
      } else {
        // Multiple Cities
        return this.weatherService.getMultipleWeather(cityIds);
      }
    }),
  );

  /**
   * Maps weather descriptions to Material Icons.
   */
  public getWeatherIcon(description: string): string {
    const desc = description.toLowerCase();
    if (desc.includes('cloud')) return 'cloud';
    if (desc.includes('rain')) return 'umbrella';
    if (desc.includes('sun') || desc.includes('clear')) return 'wb_sunny';
    if (desc.includes('snow')) return 'ac_unit';
    if (desc.includes('storm')) return 'thunderstorm';
    return 'filter_drama'; // Default icon
  }

  /**
   * Processes the raw weather description into a user-friendly string.
   */
  getFriendlyDescription(description: string): string {
    const desc = description.toLowerCase();
    // Return the translation if we have it, otherwise just capitalize the original
    return this.weatherTranslations[desc] || desc.charAt(0).toUpperCase() + desc.slice(1);
  }
}
