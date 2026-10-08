import { Component, signal } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { finalize } from 'rxjs';
import {
  AbstractControl,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  ValidationErrors,
  Validators,
} from '@angular/forms';
import { AuthService } from './core/auth.service';

@Component({
  imports: [ReactiveFormsModule],
  selector: 'app-login-page',
  styleUrl: './login-page.scss',
  templateUrl: './login-page.html',
})
export class LoginPage {
  constructor(
    private readonly authService: AuthService,
    private readonly router: Router,
  ) {}

  protected readonly registerForm = new FormGroup(
    {
      companyName: new FormControl('', {
        nonNullable: true,
        validators: [Validators.required, Validators.maxLength(150)],
      }),
      cnpj: new FormControl('', {
        nonNullable: true,
        validators: [
          Validators.required,
          Validators.pattern(/^(?:\d{14}|\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2})$/),
        ],
      }),
      fullName: new FormControl('', {
        nonNullable: true,
        validators: [Validators.required, Validators.maxLength(100)],
      }),
      cpf: new FormControl('', {
        nonNullable: true,
        validators: [
          Validators.required,
          Validators.pattern(/^(?:\d{11}|\d{3}\.\d{3}\.\d{3}-\d{2})$/),
        ],
      }),
      registerEmail: new FormControl('', {
        nonNullable: true,
        validators: [Validators.required, Validators.email, Validators.maxLength(70)],
      }),
      phone: new FormControl('', {
        nonNullable: true,
        validators: [Validators.required, Validators.maxLength(20)],
      }),
      registerPassword: new FormControl('', {
        nonNullable: true,
        validators: [Validators.required, Validators.minLength(8), Validators.maxLength(128)],
      }),
      confirmPassword: new FormControl('', {
        nonNullable: true,
        validators: [Validators.required],
      }),
    },
    { validators: matchingPasswords },
  );
  protected readonly loginForm = new FormGroup({
    email: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.email],
    }),
    password: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.minLength(6)],
    }),
    rememberMe: new FormControl(false, { nonNullable: true }),
  });
  protected readonly isRegistering = signal(false);
  protected readonly notice = signal('');
  protected readonly isSubmitting = signal(false);

  protected get email(): FormControl<string> {
    return this.loginForm.controls.email;
  }

  protected get password(): FormControl<string> {
    return this.loginForm.controls.password;
  }

  protected setRegistrationMode(registering: boolean): void {
    this.isRegistering.set(registering);
    this.notice.set('');
  }

  protected showRecoveryNotice(): void {
    this.notice.set(
      'A recuperação de senha ainda não está disponível: a API não possui esse recurso.',
    );
  }

  protected onSubmit(): void {
    if (this.isSubmitting()) {
      return;
    }
    this.notice.set('');

    const form = this.isRegistering() ? this.registerForm : this.loginForm;
    if (form.invalid) {
      form.markAllAsTouched();
      return;
    }

    this.isSubmitting.set(true);
    const request = this.isRegistering()
      ? this.authService.register({
          nome_empresa: this.registerForm.controls.companyName.value.trim(),
          cnpj: this.registerForm.controls.cnpj.value.replace(/\D/g, ''),
          nome_completo: this.registerForm.controls.fullName.value.trim(),
          cpf: this.registerForm.controls.cpf.value.replace(/\D/g, ''),
          email: this.registerForm.controls.registerEmail.value.trim(),
          telefone: this.registerForm.controls.phone.value.trim(),
          senha: this.registerForm.controls.registerPassword.value,
        })
      : this.authService.login(
          this.email.value.trim(),
          this.password.value,
          this.loginForm.controls.rememberMe.value,
        );

    request.pipe(finalize(() => this.isSubmitting.set(false))).subscribe({
      next: () => {
        void this.router.navigate(['/dashboard']);
      },
      error: (error: unknown) => {
        this.notice.set(this.getRequestError(error));
      },
    });
  }

  private getRequestError(error: unknown): string {
    if (!(error instanceof HttpErrorResponse)) {
      return 'Não foi possível concluir a solicitação. Tente novamente.';
    }
    if (typeof error.error?.detail === 'string') {
      return error.error.detail;
    }
    if (Array.isArray(error.error?.detail)) {
      return error.error.detail
        .map((issue: { msg?: string }) => issue.msg)
        .filter((message: string | undefined): message is string => !!message)
        .join(' ');
    }
    if (error.status === 0) {
      return 'Não foi possível conectar à API. Confirme se o servidor está rodando.';
    }
    return 'Não foi possível concluir a solicitação. Tente novamente.';
  }
}

function matchingPasswords(control: AbstractControl): ValidationErrors | null {
  const password = control.get('registerPassword')?.value;
  const confirmation = control.get('confirmPassword')?.value;

  return password && confirmation && password !== confirmation ? { passwordMismatch: true } : null;
}
