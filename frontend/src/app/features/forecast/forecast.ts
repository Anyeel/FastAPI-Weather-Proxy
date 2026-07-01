import { Component, inject } from '@angular/core';
import { AsyncPipe, CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { Observable, map, of, switchMap } from 'rxjs';

import { MatTableModule } from '@angular/material/table';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

import { ForecastService } from '../../core/services/forecast.service';
import { CityForecast } from '../../core/models/forecast.model';

/**
 * Component responsible for displaying the 5-day weather forecast
 * in a standardized Material Table.
 */
@Component({
  selector: 'app-forecast',
  standalone: true,
  imports: [CommonModule, AsyncPipe, MatTableModule, MatIconModule, MatProgressSpinnerModule],
  templateUrl: './forecast.html',
  styleUrls: ['./forecast.scss'],
})
export class Forecast {
  private route = inject(ActivatedRoute);
  public forecastService = inject(ForecastService);

  // Define the columns for the table
  public displayedColumns: string[] = ['time', 'icon', 'temperature', 'description'];

  /**
   * Reactive pipeline that reads city IDs from the URL and fetches their forecasts.
   */
  public forecastData$: Observable<CityForecast[]> = this.route.queryParams.pipe(
    map((params) => params['cities']),
    switchMap((citiesParam) => {
      if (!citiesParam) return of([]);
      const cityIds = citiesParam.split(',').map((id: string) => +id);
      return this.forecastService.getMultipleForecasts(cityIds);
    }),
  );

  /**
   * Maps weather descriptions to Material Icons.
   */
  getWeatherIcon(description: string): string {
    const desc = description.toLowerCase();
    if (desc.includes('clear') || desc.includes('sunny')) return 'wb_sunny';
    if (desc.includes('mist') || desc.includes('fog')) return 'density_medium';
    if (desc.includes('rain') || desc.includes('drizzle')) return 'umbrella';
    if (desc.includes('overcast')) return 'cloud';
    if (desc.includes('broken') || desc.includes('scattered')) return 'filter_drama';
    return 'cloud_queue';
  }

  /**
   * Formats the Python datetime string into a readable short date.
   */
  public formatDate(dateString: string): string {
    const safeDate = dateString.replace(' ', 'T');
    const date = new Date(safeDate);
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      hour: '2-digit',
      minute: '2-digit',
    });
  }
}
