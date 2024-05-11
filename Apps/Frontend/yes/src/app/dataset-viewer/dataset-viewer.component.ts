import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ManiaService } from '../Services/mania.service';

@Component({
  selector: 'app-dataset-viewer',
  templateUrl: './dataset-viewer.component.html',
  styleUrls: ['./dataset-viewer.component.css']
})
export class DatasetViewerComponent implements OnInit {
  csvData: any = { headers: [], rows: [] }; // Variable to hold parsed CSV data
  originalCsvData: any = { headers: [], rows: [] }; // Variable to hold original CSV data
  loading: boolean = false;
  loadingText: string = '';
  numRowsDisplayed: number = 10; // Number of rows to display initially
  numRowsPerPage: number = 10; // Number of rows to display per page
  searchTerm: string = ''; // Variable to hold the search term

  constructor(private maniaService: ManiaService, private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      const folder = params['folder'];
      const filename = params['filename'];
      if (folder && filename) {
        this.getCsvContent(folder, filename);
      }
    });
  }

  getCsvContent(folder: string, filename: string): void {
    this.loading = true;
    this.maniaService.getCsvContent(folder, filename).subscribe(
      (data) => {
        console.log('CSV Content:', data);
        // Parse CSV content into an array of objects
        this.originalCsvData = this.parseCsvContent(data);
        this.csvData = { ...this.originalCsvData }; // Initialize csvData with original data
        this.loading = false;
      },
      (error) => {
        console.error('Error fetching CSV content:', error);
        this.loading = false;
      }
    );
  }

  parseCsvContent(data: any): any {
    const content = data?.content || ''; // Get content or use empty string if undefined
    const rows = content.split('\n'); // Split content into rows
    const headers = rows[0].split(','); // First row contains headers
    const parsedData = { headers: headers, rows: [] as string[][] }; // Explicitly specify the type

    const numRowsToDisplay = Math.min(rows.length, this.numRowsDisplayed + 1); // Display initial rows plus header row

    for (let i = 1; i < numRowsToDisplay; i++) {
      const row: string[] = rows[i].split(','); // Specify type as string[]
      parsedData.rows.push(row);
    }

    return parsedData;
  }

  loadMoreRows(): void {
    this.numRowsDisplayed += this.numRowsPerPage;
    this.route.queryParams.subscribe(params => {
      const folder = params['folder'];
      const filename = params['filename'];
      if (folder && filename) {
        this.getCsvContent(folder, filename);
      }
    });
  }

  searchByUniqueId(): void {
    if (!this.searchTerm) {
      // If search term is empty, reset csvData to original data
      this.csvData = { ...this.originalCsvData };
      return;
    }

    // Perform search based on the search term
    const filteredRows = this.originalCsvData.rows.filter((row: string[]) =>
      row.some((cell: string) => cell.toLowerCase().includes(this.searchTerm.toLowerCase()))
    );

    this.csvData.rows = filteredRows;
  }
}
