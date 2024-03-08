import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface myData {
  success: boolean,
  message: string
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private loggedInStatus = false;

  constructor(private http: HttpClient) { }

  setLoggedIn(value: boolean) {
    this.loggedInStatus = value;
  }

  get isLoggedIn(): boolean{
    return this.loggedInStatus;
  }

  getUserDetails(username, password) {
    // post details to API server, return user info if correct
    return this.http.post<myData> ('/api/auth/submit', {
      username,
      password
    },{
      withCredentials: true
    });
  }

}
