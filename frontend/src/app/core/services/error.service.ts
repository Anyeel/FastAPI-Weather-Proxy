import { Injectable, signal, WritableSignal } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';

/**
 * Global service responsible for catching HTTP errors, parsing backend responses,
 * and exposing a reactive error state for the UI to display.
 */
@Injectable({
  providedIn: 'root',
})
export class ErrorService {
  // Global error state that any component can read
  public errorMessage: WritableSignal<string | null> = signal(null);

  /**
   * Clears the current global error state.
   */
  public clearError(): void {
    this.errorMessage.set(null);
  }

  /**
   * Standardized error handler to be piped into HTTP calls.
   * @param error - The HTTP error response caught by RxJS.
   * @returns An Observable that throws the formatted error message.
   */
  public handleError(error: HttpErrorResponse): Observable<never> {
    let errorMsg = 'An unknown error occurred!';

    if (error.error instanceof ErrorEvent) {
      errorMsg = `Network Error: ${error.error.message}`;
    } else {
      const backendDetail = error.error?.detail || error.message;
      errorMsg = `Error ${error.status}: ${backendDetail}`;
    }

    this.errorMessage.set(errorMsg);
    return throwError(() => new Error(errorMsg));
  }
}
