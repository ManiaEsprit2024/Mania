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
    { value: 'model1', viewValue: 'Entreprise_Model' },
    { value: 'model2', viewValue: 'BME_Entreprise_Model' },
    { value: 'model3', viewValue: 'Personal_Model'},
    { value: 'model3', viewValue: 'Entreprise_Model_SVM' },
    { value: 'model4', viewValue: 'Entreprise_Model_RandomForest'},
    { value: 'model5', viewValue: 'Entreprise_Model_LogisticRegression' },
    { value: 'model6', viewValue: 'Entreprise_Model_NeuralNetwork' },
    { value: 'model7', viewValue: 'Entreprise_Model_DecisionTree' },
    { value: 'model8', viewValue: 'Entreprise_Model_KNN' },
    { value: 'model9', viewValue: 'Entreprise_Model_GaussianNB' },
  ];
  
  loading = false;
  randomMessages = [
    'Treating the dataset...',
    'Processing dataset...',
    'Analyzing dataset...',
    'Applying treatment...',
    'Teaching the model ...'
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
