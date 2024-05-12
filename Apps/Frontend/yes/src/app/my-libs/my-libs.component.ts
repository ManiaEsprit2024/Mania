import { Component } from '@angular/core';
import { ManiaService } from '../Services/mania.service';
import { Router } from '@angular/router';
import { HttpHeaders } from '@angular/common/http';
import { TreatDialogComponentComponent } from '../treat-dialog-component/treat-dialog-component.component';
import { MatDialog } from '@angular/material/dialog';
import { Dialog } from '@angular/cdk/dialog';

@Component({
  selector: 'app-my-libs',
  templateUrl: './my-libs.component.html',
  styleUrls: ['./my-libs.component.css']
})
export class MyLibsComponent {

  libs: any[] | undefined;
  selectedFile: File | undefined;
  analyticsResult: any; // Variable to hold the analytics result
  constructor(private maniaService: ManiaService, private router: Router,private dialog: MatDialog) { }

  ngOnInit(): void {
    this.getLibraries();
  }

  getLibraries(): void {
    this.maniaService.listFilesInFolder("datasets").subscribe(
      (data) => {
        this.libs = data.files;
        console.log('List of files:', this.libs);
      },
      (error) => {
        console.error('Error fetching libraries:', error);
      }
    );
  }

  showLibrary(lib: any) {
    console.log('Showing library:', lib);
    this.router.navigate(['/dataviewer'], { queryParams: { folder: 'datasets', filename: lib } });
  }

  deleteLibrary(lib: any) {
    console.log('Deleting library:', lib);
    this.maniaService.deleteFile('datasets', lib).subscribe(
      (data) => {
        console.log(data.message);
        this.getLibraries();
      },
      (error) => {
        console.error('Error deleting library:', error);
      }
    );
  }

  uploadDataset() {
    if (this.selectedFile) {
      this.maniaService.uploadDataset(this.selectedFile, 'datasets').subscribe(
        (data) => {
          console.log(data.message);
          this.getLibraries();
        },
        (error) => {
          console.error('Error uploading dataset:', error);
        }
      );
    } else {
      console.error('No file selected.');
    }
  }
  
  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
    console.log('Selected file:', this.selectedFile);
  }

  openTreatDialog(lib: any): void {
    const dialogRef = this.dialog.open(TreatDialogComponentComponent, {
      width: '400px',
      data: { lib: lib },
    });
  
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    }); 
  }

  getAnalytics(filename: string) {
    this.maniaService.getDatasetStats(filename).subscribe(
      (response) => {
        console.log(response);
        this.analyticsResult = response;
      },
      (error) => {
        console.error('Error:', error);
      }
    );
  }
  
  getObjectKeys(obj: any): string[] {
    return Object.keys(obj || {});
  }

  downloadDataset(lib: string) {
    this.maniaService.downloadCsv('datasets', lib).subscribe(
      (data) => {
        this.downloadFile(data, lib);
      },
      (error) => {
        console.error('Error downloading dataset:', error);
      }
    );
  }

  downloadFile(data: any, filename: string) {
    const blob = new Blob([data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }
}
