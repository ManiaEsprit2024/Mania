import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { UserService } from '../user.service';
import { map } from 'rxjs/operators';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class LoginComponent implements OnInit {

  constructor(private Auth: AuthService, private router: Router) { }

  ngOnInit(): void {}

  loginUser(event): void {

    event.preventDefault();
    const targetElement = event.target;
    const username = targetElement.querySelector('#username').value;
    const password = targetElement.querySelector('#password').value;

    if(username && password){
      this.Auth.getUserDetails(username, password).subscribe(data => {
        if(data.success){
          this.Auth.setLoggedIn(true);
          this.router.navigate(['admin']);
        }else{
          window.alert(data.message);
        }
      });
    } else {
      window.alert('You need to inform an username and a password to continue.')
    }
  }
}
