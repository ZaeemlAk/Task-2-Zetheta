import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

export function DriftChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data} margin={{ bottom: 40 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="feature"
          interval={0}
          angle={-25}
          textAnchor="end"
          height={70}
        />
        <YAxis />
        <Tooltip />
        <Bar dataKey="latest_psi" fill="#10b981" name="PSI" />
      </BarChart>
    </ResponsiveContainer>
  );
}
