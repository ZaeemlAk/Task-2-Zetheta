export function StatCard({ title, value, detail, tone }) {
  return (
    <div className={`stat-card ${tone}`}>
      <div className="title">{title}</div>
      <div className="value">{value}</div>
      <div className="detail">{detail}</div>
    </div>
  );
}

export function AlertList({ alerts }) {
  return (
    <ul className="alert-list">
      {alerts.map((alert) => (
        <li
          key={`${alert.level}-${alert.title}`}
          className={`alert ${alert.level.toLowerCase()}`}
        >
          <strong>{alert.level}</strong> {alert.title}
          <div>{alert.message}</div>
        </li>
      ))}
    </ul>
  );
}

export function KeyFindings() {
  return (
    <ul className="plain-list">
      <li>First sustained drift: week 17.</li>
      <li>Critical features: F01, F10, F14, F15.</li>
      <li>
        Systemic causes: label lag, upstream data changes, and feedback loop.
      </li>
    </ul>
  );
}

export function RootCause({ fishbone }) {
  return (
    <>
      <h3>Fishbone</h3>
      <div className="root-box">
        {Object.entries(fishbone).map(([category, causes]) => (
          <div key={category} className="fishbone-group">
            <strong>{category}</strong>
            <ul>
              {causes.map((cause) => (
                <li key={cause}>{cause}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </>
  );
}

export function BusinessImpact({ business, formatCurrency }) {
  const metrics = [
    ['Estimated fraud loss', business.estimated_loss_inr],
    ['False-positive cost', business.false_positive_cost_inr],
    ['Missed fraud cost', business.missed_fraud_cost_inr],
    ['Total business impact', business.total_business_impact_inr],
  ];

  return (
    <div className="kpi-stack">
      {metrics.map(([label, value]) => (
        <div key={label}>
          <span>{label}</span>
          <strong>{formatCurrency(value)}</strong>
        </div>
      ))}
    </div>
  );
}

export function EventTimeline({ events }) {
  return (
    <div className="event-list">
      {events.map((event) => (
        <div className="event-card" key={`${event.event_date}-${event.category}`}>
          <div className="event-date">{event.event_date}</div>
          <div>
            <strong>{event.category}</strong>
            <p>{event.description}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
