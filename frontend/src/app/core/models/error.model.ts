/**
 * Helps the frontend properly type and handle FastAPI's HTTP Exceptions.
 */
export interface ApiError {
  status: number;
  message: string;
}
