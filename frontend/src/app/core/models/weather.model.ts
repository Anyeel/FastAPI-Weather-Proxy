/**
 * Matches the backend WeatherResponse model.
 * Represents current weather conditions for a specific city.
 */
export interface WeatherResponse {
  city_id: number;
  city_name: string;
  temperature: number;
  description: string;
  humidity: number;
}
