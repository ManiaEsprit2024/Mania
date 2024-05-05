import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ManiaService {

  private baseUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<any> {
    const body = {
      username,
      password
    };
    
    return this.http.post(`${this.baseUrl}/validate_mania`, body);
  }
}
