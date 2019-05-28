import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import {catchError} from 'rxjs/operators';

import { Cita } from './cita';

const httpOptions = {

    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({ providedIn: 'root' })
export class CitaService {

  private citaUrl = 'http://3ff175ef.ngrok.io';  // URL to REST API

  messageService: any;

  constructor(private http: HttpClient) { }

  /** GET users from the server */
  getCitas(): Observable<Cita[]> {

    return this.http.get<Cita[]>(this.citaUrl + '/citas').pipe(catchError(this.handleError<Cita[]>('getCitas', [])));
  }

   private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      this.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

/** Log a HeroService message with the MessageService */
  private log(message: string) {
    this.messageService.add(`HeroService: ${message}`);
  }

}