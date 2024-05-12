import { Component } from '@angular/core';
import { ManiaService } from '../Services/mania.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-treated-data',
  templateUrl: './treated-data.component.html',
  styleUrl: './treated-data.component.css'
})
export class TreatedDataComponent {
  libs: any[] | undefined;

  constructor(private maniaService: ManiaService, private router: Router) { }

  ngOnInit(): void {
    this.getLibraries();
  }

  getLibraries(): void {
    this.maniaService.listFilesInFolder("Output").subscribe(
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
    this.router.navigate(['/dataviewer'], { queryParams: { folder: 'Output', filename: lib } });
  }

  deleteLibrary(lib: any) {
    console.log('Deleting library:', lib);
    this.maniaService.deleteFile('output', lib).subscribe(
      (data) => {
        console.log(data.message);
        this.getLibraries();
      },
      (error) => {
        console.error('Error deleting library:', error);
      }
    );
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
