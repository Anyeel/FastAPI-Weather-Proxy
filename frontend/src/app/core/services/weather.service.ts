import { inject, Injectable, signal, WritableSignal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, finalize, Observable } from 'rxjs';

import { WeatherResponse } from '../models/weather.model';
import { ErrorService } from './error.service';

import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class WeatherService {
  private readonly apiUrl = `${environment.apiUrl}/weather`;

  // State Management
  public isLoading: WritableSignal<boolean> = signal(false);
  public errorMessage: WritableSignal<string | null> = signal(null);

  private http = inject(HttpClient);
  private errorService = inject(ErrorService);

  // First endpoint: weather on a single city
  getSingleWeather(cityId: number): Observable<WeatherResponse> {
    this.resetState();

    return this.http.get<WeatherResponse>(`${this.apiUrl}/${cityId}`).pipe(
      catchError((err) => this.errorService.handleError(err)),
      finalize(() => this.isLoading.set(false)),
    );
  }

  // Second endpoint: get weather on multiple cities
  getMultipleWeather(cityIds: number[]): Observable<WeatherResponse[]> {
    this.resetState();
    const params = { cities: cityIds.join(',') };

    return this.http.get<WeatherResponse[]>(this.apiUrl, { params }).pipe(
      catchError((err) => this.errorService.handleError(err)),
      finalize(() => this.isLoading.set(false)),
    );
  }

  private resetState(): void {
    this.isLoading.set(true);
    this.errorMessage.set(null);
    this.errorService.clearError();
  }
}
