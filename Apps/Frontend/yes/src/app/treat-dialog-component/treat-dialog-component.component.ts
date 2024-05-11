import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ManiaService } from '../Services/mania.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-treat-dialog-component',
  templateUrl: './treat-dialog-component.component.html',
  styleUrls: ['./treat-dialog-component.component.css']
})
export class TreatDialogComponentComponent {
  selectedModel: string | undefined;
  models = [
    { value: 'model1', viewValue: 'Model 1' },
    { value: 'model2', viewValue: 'Big Medium Entreprise Model' },
    { value: 'model3', viewValue: 'Individuals Model' },
  ];
  loading = false;
  randomMessages = [
    'Treating the dataset...',
    'Processing dataset...',
    'Analyzing dataset...',
    'Applying treatment...'
  ];
  randomMessage = '';

  constructor(
    public dialogRef: MatDialogRef<TreatDialogComponentComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private maniaService: ManiaService,
    private router: Router
  ) {}

  closeDialog(): void {
    if (!this.loading) {
      this.dialogRef.close();
    }
  }

  submitForm(): void {
    this.loading = true;
    const intervalId = setInterval(() => {
      const randomIndex = Math.floor(Math.random() * this.randomMessages.length);
      this.randomMessage = this.randomMessages[randomIndex];
    }, 3000); 
    this.maniaService.predictFicoDataset(this.data.lib).subscribe(
      (response) => {
        clearInterval(intervalId);
        this.loading = false;
        this.router.navigate(['/treated']);
        this.dialogRef.close();
      },
      (error) => {
        clearInterval(intervalId);
        this.loading = false;
        this.router.navigate(['/treated']);
        this.dialogRef.close();
      }
    );
  }
}
