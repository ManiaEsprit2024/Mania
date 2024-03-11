import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string | undefined;
  password: string | undefined;

  constructor(private router: Router) {}

  login() {
    // Simulate authentication logic with fake backend
    if (this.username === 'admin' && this.password === 'password') {
      // If authentication succeeds, redirect to dashboard or desired page
      this.router.navigate(['/dashboard']);
    } else {
      // If authentication fails, show error message or handle accordingly
      alert('Invalid username or password');
      this.router.navigate(['/dashboard']);
    }
  }
}
