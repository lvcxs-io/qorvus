import { HttpInterceptorFn } from '@angular/common/http';

import { API_BASE_URL, AUTH_TOKEN_KEY } from './api';

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  if (!request.url.startsWith(API_BASE_URL) || typeof sessionStorage === 'undefined') {
    return next(request);
  }

  const token =
    sessionStorage.getItem(AUTH_TOKEN_KEY) ??
    (typeof localStorage !== 'undefined' ? localStorage.getItem(AUTH_TOKEN_KEY) : null);
  return next(
    token ? request.clone({ setHeaders: { Authorization: `Bearer ${token}` } }) : request,
  );
};
