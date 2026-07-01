import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { toObservable } from '@angular/core/rxjs-interop';
import { Observable, of, catchError } from 'rxjs';

import { CitySearchResponse } from '../models/city.model';
import { ErrorService } from './error.service';

import { environment } from '../../../environments/environment';

/**
 * Service responsible for searching cities via the proxy backend
 * and managing the global state of user-selected cities.
 */
@Injectable({
  providedIn: 'root',
})
export class CityService {
  private readonly apiUrl = `${environment.apiUrl}/weather`;

  private http = inject(HttpClient);
  private errorService = inject(ErrorService);

  // Global State
  public selectedCities = signal<CitySearchResponse[]>([]);

  public searchCities(query: string): Observable<CitySearchResponse[]> {
    if (!query || query.trim().length < 2) {
      return of([]);
    }

    this.errorService.clearError();

    return this.http
      .get<CitySearchResponse[]>(`${this.apiUrl}/search`, {
        params: { q: query },
      })
      .pipe(catchError(this.errorService.handleError.bind(this.errorService)));
  }

  /**
   * Adds a city to the global selection state if it doesn't already exist.
   */
  public addCity(city: CitySearchResponse): void {
    const currentCities = this.selectedCities();
    if (!currentCities.find((c) => c.id === city.id)) {
      this.selectedCities.set([...currentCities, city]);
    }
  }

  /**
   * Removes a city from the global selection state by ID.
   */
  public removeCity(cityId: number): void {
    this.selectedCities.update((cities) => cities.filter((c) => c.id !== cityId));
  }
}
