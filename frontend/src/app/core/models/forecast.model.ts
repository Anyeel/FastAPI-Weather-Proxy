/**
 * Represents a single 3-hour forecast block.
 */
export interface ForecastItem {
  timestamp: string;
  temperature: number;
  description: string;
}

/**
 * Matches the backend CityForecast model.
 * Groups an array of forecast items under a specific city.
 */
export interface CityForecast {
  city_id: number;
  city_name: string;
  forecasts: ForecastItem[];
}
