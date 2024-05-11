import { Component } from '@angular/core';

@Component({
  selector: 'app-credit-checker',
  templateUrl: './credit-checker.component.html',
  styleUrls: ['./credit-checker.component.css']
})
export class CreditCheckerComponent {
  currentStep: number = 1; // Initialize with default value
  loading: boolean = false;
  loadingText: string = '';

  navigateToStep2(searchValue: string) {
    if (searchValue.trim() !== '') {
      this.startLoadingAnimation();
      setTimeout(() => {
        this.currentStep = 3; // Move to step 3 after 3 seconds
        this.loading = false;
      }, 3000); // 3 seconds delay
    }
  }

  startLoadingAnimation() {
    this.loading = true;
    this.updateLoadingText();
    setTimeout(() => {
      this.loading = false;
      this.loadingText = '';
    }, 3000);
  }

  updateLoadingText() {
    const texts = [
      "Loading some data...",
      "Preparing your dashboard...",
      "Fetching information...",
      "Hold on, almost there..."
    ];
    let index = 0;

    // Update loading text every 1.5 seconds
    const intervalId = setInterval(() => {
      this.loadingText = texts[index];
      index = (index + 1) % texts.length;
    }, 1500);

    // Stop updating loading text after 3 seconds
    setTimeout(() => {
      clearInterval(intervalId);
    }, 3000);
  }
}
