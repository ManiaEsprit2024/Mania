import { Component } from '@angular/core';
import { ManiaService } from '../Services/mania.service';

@Component({
  selector: 'app-calculator',
  templateUrl: './calculator.component.html',
  styleUrls: ['./calculator.component.css']
})
export class CalculatorComponent {
  formData: any = {};
  years: number[] = Array.from({length: 8}, (_, i) => 2010 + i);
  result: any; // To store the prediction result

  constructor(private maniaService: ManiaService) {}

  submitForm() {
    this.formData.optional_revenue_yr_confirmed = parseInt(this.formData.optional_revenue_yr_confirmed);
    this.maniaService.predictFicoSE(this.formData)
      .subscribe((response: any[]) => {
        if (response.length > 0) {
          this.result = response[0]; // Extract the result object from the array
          console.log('Response:', this.result);
        } else {
          console.error('Error: Empty response');
        }
      }, (error) => {
        console.error('Error:', error);
        // Handle error here
      });
  }  
}
