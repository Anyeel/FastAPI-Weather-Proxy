import { Component, inject, OnInit, signal, ViewChild, ElementRef } from '@angular/core';
import { Router } from '@angular/router';
import { FormControl, ReactiveFormsModule } from '@angular/forms';

import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import {
  MatAutocompleteModule,
  MatAutocompleteSelectedEvent,
} from '@angular/material/autocomplete';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';

import { WeatherService } from '../../services/weather.service';
import { ErrorService } from '../../services/error.service';
import { CityService } from '../../services/city.service';
import { CitySearchResponse } from '../../models/city.model';
import { debounceTime, distinctUntilChanged, filter, catchError, of, switchMap } from 'rxjs';

/**
 * Global header component providing the multi-city search bar,
 * selected city chip grid, and global navigation controls.
 */
@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatFormFieldModule,
    MatButtonModule,
    MatProgressBarModule,
    MatIconModule,
    MatChipsModule,
    MatAutocompleteModule,
  ],
  templateUrl: './header.html',
  styleUrls: ['./header.scss'],
})
export class Header implements OnInit {
  private router = inject(Router);
  public cityService = inject(CityService);
  public weatherService = inject(WeatherService);
  public errorService = inject(ErrorService);

  public searchControl = new FormControl('');
  public searchResults = signal<CitySearchResponse[]>([]);
  public isSearching = signal<boolean>(false);

  @ViewChild('cityInput') cityInput!: ElementRef<HTMLInputElement>;

  ngOnInit() {
    // The reactive search pipeline
    this.searchControl.valueChanges
      .pipe(
        debounceTime(400), // Wait 400ms after the last keystroke
        distinctUntilChanged(), // Only trigger if the text actually changed
        filter((query): query is string => {
          if (!query || query.length < 2) {
            this.searchResults.set([]); // Clear results if query is too short
            return false;
          }
          return true;
        }),
        switchMap((query) => {
          this.isSearching.set(true);
          return this.cityService.searchCities(query).pipe(
            catchError(() => of([])), // If API fails, return empty array safely
          );
        }),
      )
      .subscribe((results) => {
        this.searchResults.set(results);
        this.isSearching.set(false);
      });
  }

  /**
   * Navigates to the Current Weather view passing the selected city IDs.
   */
  onCurrentWeatherClick() {
    const ids = this.cityService.selectedCities().map((c) => c.id);
    if (ids.length > 0) {
      this.router.navigate(['/current'], { queryParams: { cities: ids.join(',') } });
    }
  }

  /**
   * Navigates to the 5-Day Forecast view passing the selected city IDs.
   */
  onForecastClick() {
    // Read from the GLOBAL service
    const ids = this.cityService.selectedCities().map((c) => c.id);
    if (ids.length > 0) {
      this.router.navigate(['/forecast'], { queryParams: { cities: ids.join(',') } });
    }
  }

  /**
   * Adds a selected city from the autocomplete dropdown to the global state.
   */
  citySelected(event: MatAutocompleteSelectedEvent): void {
    const city = event.option.value as CitySearchResponse;
    this.cityService.addCity(city);

    // Clear the search box for the next input
    if (this.cityInput?.nativeElement) {
      this.cityInput.nativeElement.value = '';
    }
    this.searchControl.setValue('');
    this.searchResults.set([]);
  }

  /**
   * Removes a city from the global selection state via the chip grid.
   */
  removeCity(cityToRemove: CitySearchResponse): void {
    this.cityService.removeCity(cityToRemove.id);
  }
}
