import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ManiaService {

  private baseUrl = 'http://localhost:3000';

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<any> {
    const headers = {
      username,
      password
    };
    return this.http.post(`${this.baseUrl}/auth/submit`, null, { headers });
  }

  logout(): Observable<any> {
    return this.http.get(`${this.baseUrl}/logout`);
  }

  checkLogin(): Observable<any> {
    return this.http.get(`${this.baseUrl}/auth/check`);
  }

  getData(): Observable<any> {
    return this.http.get(`${this.baseUrl}/getData`);
  }
}
