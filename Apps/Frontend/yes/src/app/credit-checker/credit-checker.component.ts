import { Component } from '@angular/core';
import { ManiaService } from '../Services/mania.service';

@Component({
  selector: 'app-credit-checker',
  templateUrl: './credit-checker.component.html',
  styleUrls: ['./credit-checker.component.css']
})
export class CreditCheckerComponent {
  currentStep: number = 1; // Initialize with default value
  loading: boolean = false;
  loadingText: string = '';
  files: string[] | undefined;
  selectedFile: string | undefined;
  ficoScoreData: any | undefined;

  constructor(private maniaService: ManiaService) { }

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

  ngOnInit(): void {
    this.getOutputFiles();
  }

  updateLoadingText() {
    const texts = [
      "Loading some data...",
      "Preparing your dashboard...",
      "Fetching information...",
      "Hold on, almost there..."
    ];
    let index = 0;

    const intervalId = setInterval(() => {
      this.loadingText = texts[index];
      index = (index + 1) % texts.length;
    }, 1500);

    // Stop updating loading text after 3 seconds
    setTimeout(() => {
      clearInterval(intervalId);
    }, 3000);

  }

  getOutputFiles(): void {
    this.maniaService.listFilesInFolder('output').subscribe(
      (data: any) => {
        this.files = data.files;
        console.log('List of output files:', this.files);
      },
      (error) => {
        console.error('Error fetching output files:', error);
      }
    );
  }

  searchFicoScore(uniqueId: string): void {
    this.loading = true;
    if (this.selectedFile) {
      this.maniaService.getFicoScoreByUniqueId(this.selectedFile, uniqueId).subscribe(
        (data) => {
          console.log('FICO Score:', data);
          this.loading = false;
          if (data.fico_score === 'invalid unique_id') {
            console.error('Invalid unique ID:', uniqueId);
          } else {
            this.currentStep = 3;
            this.ficoScoreData = data.fico_score;
          }
        },
        (error) => {
          console.error('Error fetching FICO score:', error);
          this.loading = false;
        }
      );
    }
  }

}
