import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { API_BASE_URL } from './api';
import { Company, DashboardSummary } from './auth.models';

@Injectable({ providedIn: 'root' })
export class DashboardService {
  constructor(private readonly http: HttpClient) {}

  getSummary(): Observable<DashboardSummary> {
    return this.http.get<DashboardSummary>(`${API_BASE_URL}/dashboard/resumo`);
  }

  getCompany(): Observable<Company> {
    return this.http.get<Company>(`${API_BASE_URL}/empresas/minha`);
  }
}
