import { useEffect, useState } from 'react';
import { DriftChart } from './charts/DriftChart';
import { PerformanceChart } from './charts/PerformanceChart';
import {
  AlertList,
  BusinessImpact,
  EventTimeline,
  KeyFindings,
  RootCause,
  StatCard,
} from './components/DashboardSections';
import { getDashboardData } from './services/dashboardService';

function formatCurrency(value) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(value);
}

export default function App() {
  const [dashboard, setDashboard] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;

    getDashboardData()
      .then((data) => {
        if (active) {
          setDashboard(data);
        }
      })
      .catch((requestError) => {
        console.error('Unable to load the investigation dashboard.', requestError);
        if (active) {
          setError(
            requestError.response?.data?.detail ||
              'Could not connect to the backend. Confirm that the API is running and try refreshing.'
          );
        }
      });

    return () => {
      active = false;
    };
  }, []);

  if (error) {
    return (
      <main className="page-shell">
        <section className="panel error-panel" role="alert">
          <h1>Dashboard unavailable</h1>
          <p>{error}</p>
        </section>
      </main>
    );
  }

  if (!dashboard) {
    return <div className="loading">Loading SENTINEL-7 investigation dashboard…</div>;
  }

  const {
    performance,
    timeline,
    drift,
    rootCause,
    modelHealth,
    events,
    business,
  } = dashboard;

  return (
    <div className="page-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">National Prosperity Bank</p>
          <h1>SENTINEL-7 Drift Investigation</h1>
        </div>
        <div className="badge status-badge">{modelHealth.status}</div>
      </header>

      <section className="stats-grid">
        <StatCard
          title="Model health"
          value={`${modelHealth.overall_score}/100`}
          detail={modelHealth.status}
          tone="critical"
        />
        <StatCard
          title="Precision"
          value={`${(performance.precision * 100).toFixed(1)}%`}
          detail="Current"
          tone="warning"
        />
        <StatCard
          title="Recall"
          value={`${(performance.recall * 100).toFixed(1)}%`}
          detail="Current"
          tone="warning"
        />
        <StatCard
          title="Estimated exposure"
          value={formatCurrency(business.estimated_exposure_inr)}
          detail="INR"
          tone="danger"
        />
      </section>

      <section className="chart-grid">
        <div className="panel chart-panel wide">
          <h2>Performance timeline</h2>
          <PerformanceChart data={timeline} />
        </div>
        <div className="panel">
          <h2>Alert status</h2>
          <AlertList alerts={modelHealth.alerts} />
        </div>
      </section>

      <section className="chart-grid">
        <div className="panel wide">
          <h2>Top drift features</h2>
          <DriftChart data={drift.slice(0, 8)} />
        </div>
        <div className="panel">
          <h2>Key findings</h2>
          <KeyFindings />
        </div>
      </section>

      <section className="two-col">
        <div className="panel">
          <h2>Root-cause investigation</h2>
          <RootCause fishbone={rootCause.fishbone} />
        </div>
        <div className="panel">
          <h2>Business impact</h2>
          <BusinessImpact business={business} formatCurrency={formatCurrency} />
        </div>
      </section>

      <section className="panel">
        <h2>External events timeline</h2>
        <EventTimeline events={events} />
      </section>
    </div>
  );
}
