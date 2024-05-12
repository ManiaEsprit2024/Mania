import { Component } from '@angular/core';
import { Chart } from 'angular-highcharts';
import { ManiaService } from '../Services/mania.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  isLoading: boolean = true;
  loadingText: string = '';
  private intervalId: any;
  pieChart: Chart;
  barChart: Chart;
  chartData: any;

  constructor(private maniaService: ManiaService) {
    this.pieChart = new Chart({
      title: {
        text: 'Customers Data'
      },
      series: [{
        type: 'pie',
        data: [
          { name: 'SE', y: 10, color: '#eeeeee' },
          { name: 'BME', y:30, color: '#393e64' },
          { name: 'Individuals', y: 200, color: '#000000' }
        ]
      }]
    });

    this.barChart = new Chart({
      chart: {
        type: 'bar'
      },
      title: {
        text: 'Log Data'
      },
      series: [{
           name: 'Log Data', data: [Math.floor(Math.random() * 10)], // Initialize with random data
      } as any]
    });
  }

  ngOnInit(): void {
    this.fetchChartDataFromService();
    // Simulating some asynchronous operation that triggers the spinner
    setTimeout(() => {
      this.isLoading = false;
      this.clearInterval();
    }, 0);

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

  fetchChartDataFromService(): void {
    this.maniaService.extractChartDataFromLogs().subscribe(
      (data: any) => {
        this.chartData = data.chart_data;
      },
      (error: any) => {
        console.error('Error fetching customer data:', error);
      }
    );
  }
}
