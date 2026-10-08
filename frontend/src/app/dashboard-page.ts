import { Component, computed, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';

import { AuthUser, Company, DashboardSummary } from './core/auth.models';
import { AuthService } from './core/auth.service';
import { DashboardService } from './core/dashboard.service';

type NavigationItem = {
  label: string;
  icon: 'home' | 'box' | 'history' | 'chart' | 'users';
};

@Component({
  imports: [RouterLink],
  selector: 'app-dashboard-page',
  styleUrl: './dashboard-page.scss',
  templateUrl: './dashboard-page.html',
})
export class DashboardPage {
  private readonly authService = inject(AuthService);
  private readonly dashboardService = inject(DashboardService);
  private readonly router = inject(Router);

  protected readonly mobileMenuOpen = signal(false);
  protected readonly navigationNotice = signal('');
  protected readonly loading = signal(true);
  protected readonly loadError = signal('');
  protected readonly summary = signal<DashboardSummary | null>(null);
  protected readonly company = signal<Company | null>(null);
  protected readonly user = signal<AuthUser | null>(this.authService.currentUser());

  protected readonly primaryNavigation: NavigationItem[] = [
    { label: 'Visão geral', icon: 'home' },
    { label: 'Catálogo', icon: 'box' },
    { label: 'Histórico', icon: 'history' },
    { label: 'Relatórios', icon: 'chart' },
  ];

  protected readonly chartPoints = computed(() => this.makeChartPoints('entradas'));
  protected readonly movementPoints = computed(() => this.makeChartPoints('saidas'));
  protected readonly entriesPath = computed(() => this.makeLinePath(this.chartPoints()));
  protected readonly exitsPath = computed(() => this.makeLinePath(this.movementPoints()));
  protected readonly entriesAreaPath = computed(() => this.makeAreaPath(this.chartPoints()));
  protected readonly chartDates = computed(() => {
    const series = this.summary()?.serie_movimentacoes ?? [];
    return series.map((day) =>
      new Intl.DateTimeFormat('pt-BR', { weekday: 'short' })
        .format(new Date(`${day.data}T12:00:00`))
        .replace('.', ''),
    );
  });
  protected readonly chartScale = computed(() =>
    Math.max(
      1,
      ...(this.summary()?.serie_movimentacoes ?? []).flatMap((day) => [day.entradas, day.saidas]),
    ),
  );
  protected readonly lowStockItems = computed(() =>
    (this.summary()?.produtos_estoque_baixo ?? []).map((item) => ({
      ...item,
      unit: item.quantidade === 1 ? 'unidade' : 'unidades',
      level: Math.max(
        8,
        Math.min(100, Math.round((item.quantidade / Math.max(item.limite_minimo, 1)) * 100)),
      ),
    })),
  );
  protected readonly recentMovements = computed(() =>
    (this.summary()?.movimentacoes_recentes ?? []).map((movement) => ({
      ...movement,
      detail: movement.tipo === 'ENTRADA' ? 'Entrada de estoque' : 'Saída de estoque',
      time: new Intl.DateTimeFormat('pt-BR', {
        hour: '2-digit',
        minute: '2-digit',
      }).format(new Date(movement.data_hora)),
      date: new Intl.DateTimeFormat('pt-BR').format(new Date(movement.data_hora)),
      type: movement.tipo === 'ENTRADA' ? 'entry' : 'exit',
      quantity: `${movement.tipo === 'ENTRADA' ? '+' : '−'}${movement.quantidade} un.`,
    })),
  );
  protected readonly todayLabel = new Intl.DateTimeFormat('pt-BR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(new Date());

  constructor() {
    forkJoin({
      summary: this.dashboardService.getSummary(),
      company: this.dashboardService.getCompany(),
      user: this.authService.loadCurrentUser(),
    }).subscribe({
      next: ({ summary, company, user }) => {
        this.summary.set(summary);
        this.company.set(company);
        this.user.set(user);
        this.loading.set(false);
      },
      error: (error: unknown) => {
        this.loading.set(false);
        if (this.isUnauthorized(error)) {
          this.authService.logout();
          void this.router.navigate(['/']);
          return;
        }
        this.loadError.set(
          'Não foi possível carregar os dados do painel. Confira se a API e o banco estão disponíveis.',
        );
      },
    });
  }

  protected showSectionNotice(label: string): void {
    this.navigationNotice.set(
      `${label} será a próxima etapa do protótipo. Por enquanto, esta é a visão geral.`,
    );
    this.mobileMenuOpen.set(false);
  }

  protected toggleMobileMenu(): void {
    this.mobileMenuOpen.update((isOpen) => !isOpen);
  }

  protected dismissSectionNotice(): void {
    this.navigationNotice.set('');
  }

  protected logout(): void {
    this.authService.logout();
    void this.router.navigate(['/']);
  }

  private makeChartPoints(key: 'entradas' | 'saidas'): { x: number; y: number }[] {
    const series = this.summary()?.serie_movimentacoes ?? [];
    const maxValue = this.chartScale();
    const step = series.length > 1 ? 612 / (series.length - 1) : 0;

    return series.map((day, index) => ({
      x: series.length > 1 ? 30 + index * step : 336,
      y: 152 - (day[key] / maxValue) * 112,
    }));
  }

  private makeLinePath(points: { x: number; y: number }[]): string {
    return points
      .map((point, index) => `${index === 0 ? 'M' : 'L'} ${point.x} ${point.y}`)
      .join(' ');
  }

  private makeAreaPath(points: { x: number; y: number }[]): string {
    if (points.length === 0) {
      return '';
    }
    return `${this.makeLinePath(points)} L ${points[points.length - 1].x} 152 L ${points[0].x} 152 Z`;
  }

  private isUnauthorized(error: unknown): boolean {
    return typeof error === 'object' && error !== null && 'status' in error && error.status === 401;
  }
}
