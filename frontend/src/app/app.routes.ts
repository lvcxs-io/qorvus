import { Routes } from '@angular/router';
import { DashboardPage } from './dashboard-page';
import { LoginPage } from './login-page';
import { authenticatedGuard } from './core/auth.guard';

export const routes: Routes = [
  { path: '', component: LoginPage, title: 'Entrar | Qorvus' },
  {
    path: 'dashboard',
    component: DashboardPage,
    canActivate: [authenticatedGuard],
    title: 'Visão geral | Qorvus',
  },
  { path: '**', redirectTo: '' },
];
