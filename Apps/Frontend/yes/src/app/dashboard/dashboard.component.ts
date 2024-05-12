import { Component } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  isLoading: boolean = true;
  loadingText: string = '';
  private intervalId: any;

  constructor() { }

  ngOnInit(): void {
    // Simulating some asynchronous operation that triggers the spinner
    setTimeout(() => {
      this.isLoading = false;
      this.clearInterval();
    }, 7000);

    // Start interval to update loading text dynamically
    this.intervalId = setInterval(() => {
      this.loadingText = this.generateRandomText();
    }, 1500);
  }

  generateRandomText(): string {
    const texts = [
      "Preparing your dashboard...",
    ];

    return texts[Math.floor(Math.random() * texts.length)];
  }

  ngOnDestroy(): void {
    this.clearInterval();
  }

  private clearInterval(): void {
    // Clear interval to avoid memory leaks
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }
}
