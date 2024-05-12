import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ManiaService {

  private baseUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<any> {
    const body = {
      username,
      password
    };
    
    return this.http.post(`${this.baseUrl}/validate_mania`, body);
  }

  getFicoScoreByUniqueId(outputFile: string, uniqueId: string): Observable<any> {
    const body = { output_file: outputFile, unique_id: uniqueId };
    return this.http.post(`${this.baseUrl}/get_fico_by_unique_id`, body);
  }
  
  uploadDataset(csvFile: File, folder: string): Observable<any> {
    const formData = new FormData();
    formData.append('csv_file', csvFile);
    formData.append('folder', folder);
    return this.http.post(`${this.baseUrl}/upload_dataset`, formData);
  }

  getCsvContent(folder: string, filename: string): Observable<any> {
    const body = { folder, filename };
    return this.http.post(`${this.baseUrl}/get_csv_content`, body);
  }

  listFilesInFolder(folder: string): Observable<any> {
    const body = { folder };
    return this.http.post(`${this.baseUrl}/list_files_in_folder`, body);
  }

  deleteFile(folder: string, filename: string): Observable<any> {
    const body = { folder, filename };
    return this.http.post(`${this.baseUrl}/delete_file`, body);
  }

  predictFicoDataset(datasetName: string): Observable<any> {
    const body = { dataset_name: datasetName };
    return this.http.post(`${this.baseUrl}/predict_fico_dataset`, body);
  }
  
  predictFicoSE(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/predict_fico_se`, data);
  }

  getDatasetStats(filename: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/dataset_stats`, { filename });
  }
}
