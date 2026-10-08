import { HttpClient } from '@angular/common/http';
import { Injectable, signal } from '@angular/core';
import { Observable, tap } from 'rxjs';

import { API_BASE_URL, AUTH_TOKEN_KEY } from './api';
import { AuthResponse, AuthUser, CompanyRegistration } from './auth.models';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly currentUserState = signal<AuthUser | null>(null);
  readonly currentUser = this.currentUserState.asReadonly();

  constructor(private readonly http: HttpClient) {}

  register(data: CompanyRegistration): Observable<AuthResponse> {
    return this.http
      .post<AuthResponse>(`${API_BASE_URL}/auth/register`, data)
      .pipe(tap((response) => this.acceptSession(response)));
  }

  login(email: string, senha: string, rememberMe = false): Observable<AuthResponse> {
    return this.http
      .post<AuthResponse>(`${API_BASE_URL}/auth/login`, { email, senha })
      .pipe(tap((response) => this.acceptSession(response, rememberMe)));
  }

  logout(): void {
    if (typeof sessionStorage !== 'undefined') {
      sessionStorage.removeItem(AUTH_TOKEN_KEY);
    }
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem(AUTH_TOKEN_KEY);
    }
    this.currentUserState.set(null);
  }

  loadCurrentUser(): Observable<AuthUser> {
    return this.http
      .get<AuthUser>(`${API_BASE_URL}/auth/me`)
      .pipe(tap((user) => this.currentUserState.set(user)));
  }

  hasToken(): boolean {
    return this.getStoredToken() !== null;
  }

  private acceptSession(response: AuthResponse, rememberMe = false): void {
    if (typeof sessionStorage === 'undefined') {
      throw new Error('O login requer um navegador com armazenamento de sessão habilitado.');
    }
    if (rememberMe && typeof localStorage !== 'undefined') {
      localStorage.setItem(AUTH_TOKEN_KEY, response.access_token);
    } else {
      sessionStorage.setItem(AUTH_TOKEN_KEY, response.access_token);
    }
    this.currentUserState.set(response.user);
  }

  private getStoredToken(): string | null {
    if (typeof sessionStorage === 'undefined') {
      return null;
    }
    return (
      sessionStorage.getItem(AUTH_TOKEN_KEY) ??
      (typeof localStorage !== 'undefined' ? localStorage.getItem(AUTH_TOKEN_KEY) : null)
    );
  }
}
