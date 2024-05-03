import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormControl, FormGroup } from '@angular/forms';
import { ManiaService } from '../Services/mania.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  profileForm = new FormGroup({
    username: new FormControl(''),
    password: new FormControl(''),
  });
  loginResponse: string | null = null;

  constructor(private backendService: ManiaService, private router: Router) {}

  login() {
    const { username, password } = this.profileForm.value;

    if (username && password) {
      this.backendService.login(username, password).subscribe(
        (response) => {
          if (response.message === 'OK') {
            this.router.navigate(['/dashboard']);
          } else {
            this.loginResponse = response.message;
          }
        },
        (error) => {
          this.loginResponse = error.error.message;
        }
      );
    }
  }
}
