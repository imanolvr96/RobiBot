import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import {catchError} from 'rxjs/operators';

import { Horario } from './horario';

const httpOptions = {

    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({ providedIn: 'root' })
export class HorarioService {

  private horarioUrl = 'http://a4fa2f4a.ngrok.io';  // URL to REST API
  messageService: any;

  constructor(private http: HttpClient) { }

  /** GET users from the server */
  getHorarios(): Observable<Horario[]> {

    return this.http.get<Horario[]>(this.horarioUrl + '/horarios').pipe(catchError(this.handleError<Horario[]>('getHorarios', [])));
  }

    /** DELETE RESERVATION */
  deleteHour(horario: Horario | number) {

    const id = typeof horario === 'number' ? horario : horario.id;
    const url = `${this.horarioUrl}/deleteH/${id}`;
    return this.http.delete(url, httpOptions);
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