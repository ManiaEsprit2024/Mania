import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { CreditCheckerComponent } from './credit-checker/credit-checker.component';
import { MyLibsComponent } from './my-libs/my-libs.component';
import { TreatedDataComponent } from './treated-data/treated-data.component';
import { DatasetViewerComponent } from './dataset-viewer/dataset-viewer.component';
import { CalculatorComponent } from './calculator/calculator.component';
import { DocumentationComponent } from './documentation/documentation.component';
import { ChatbotComponent } from './chatbot/chatbot.component';
import { LogsComponent } from './logs/logs.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: '', component: HomeComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'checker', component: CreditCheckerComponent },
  { path: 'libs', component: MyLibsComponent },
  { path: 'treated', component: TreatedDataComponent },
  { path: 'dataviewer', component: DatasetViewerComponent },
  { path: 'calculator', component: CalculatorComponent },
  { path: 'docs', component: DocumentationComponent },
  { path: 'maniamini', component: ChatbotComponent },
  { path: 'logs', component: LogsComponent },
];
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { 
}
