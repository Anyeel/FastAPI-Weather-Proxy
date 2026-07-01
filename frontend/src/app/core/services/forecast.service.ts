import { Injectable, inject, signal, WritableSignal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ErrorService } from './error.service';
import { CityForecast } from '../models/forecast.model';
import { catchError, finalize, Observable } from 'rxjs';

import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ForecastService {
  private readonly apiUrl = `${environment.apiUrl}/forecast`;

  // State Management
  public isLoading: WritableSignal<boolean> = signal(false);
  public errorMessage: WritableSignal<string | null> = signal(null);

  private http = inject(HttpClient);
  private errorService = inject(ErrorService);

  // Third Endpoint
  getMultipleForecasts(cityIds: number[]): Observable<CityForecast[]> {
    this.prepareRequest();
    const params = { cities: cityIds.join(',') };

    return this.http.get<CityForecast[]>(this.apiUrl, { params }).pipe(
      catchError(this.errorService.handleError.bind(this.errorService)),
      finalize(() => this.isLoading.set(false)),
    );
  }

  private prepareRequest(): void {
    this.isLoading.set(true);
    this.errorMessage.set(null);
    this.errorService.clearError();
  }
}
