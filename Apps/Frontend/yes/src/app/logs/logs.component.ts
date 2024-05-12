import { Component } from '@angular/core';
import { ManiaService } from '../Services/mania.service';

@Component({
  selector: 'app-logs',
  templateUrl: './logs.component.html',
  styleUrl: './logs.component.css'
})
export class LogsComponent {
  logsContent: any | undefined;

  constructor(private maniaService: ManiaService) {}
  ngOnInit(): void {
    this.fetchLogs();
  }

  fetchLogs(): void {
    this.maniaService.downloadLogFile().subscribe(
      (response: any) => { // Specify type for response
        this.logsContent = this.prettifyLogs(this.prettifyJson(response));
      },
      (error: any) => { // Specify type for error
        console.error(error);
        this.logsContent = "Error fetching logs: " + error.message;
      }
    );
  }

  prettifyJson(json: any): string {
    return JSON.stringify(json, null, 2);
  }

  prettifyLogs(logs: string): any[] {
    try {
      logs = logs.replace(/\\n/g, '\n');
      return logs.split('\n').map(line => {
        const color = this.getColor(line);
        return { text: line.substring(20), color };
      });
    } catch (error) {
      console.error("Error parsing logs:", error);
      return [{ text: "Error parsing logs.", color: 'black' }];
    }
  }

  getColor(line: string): string {
    if (line.includes('INFO')) {
      return 'green';
    } else if (line.includes('WARNING')) {
      return 'orange';
    } else if (line.includes('ERROR')) {
      return 'red';
    } else {
      return 'black';
    }
  }
  
}
