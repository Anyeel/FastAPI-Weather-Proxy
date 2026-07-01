import { Routes } from '@angular/router';
import { Home } from './features/home/home';
import { CurrentWeather } from './features/current-weather/current-weather';
import { Forecast } from './features/forecast/forecast';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'current', component: CurrentWeather },
  { path: 'forecast', component: Forecast },
  { path: '**', redirectTo: '' }, // Catch-all redirects to home
];
