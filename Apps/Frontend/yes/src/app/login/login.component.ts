import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { ManiaService } from '../Services/mania.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  profileForm = new FormGroup({
    username: new FormControl(''),
    password: new FormControl(''),
  });
  loginResponse: string | null = null;

  constructor(private backendService: ManiaService) {}

  login() {
    if(this.profileForm.value.username && this.profileForm.value.password)
    this.backendService.login(this.profileForm.value.username,this.profileForm.value.password).subscribe((response) => {
      this.loginResponse = response.message;
    }, (error) => {
      this.loginResponse = error.error.message;
    });
  }
}