import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

export function PerformanceChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="week_id" />
        <YAxis domain={[0.5, 1]} />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="precision"
          stroke="#3b82f6"
          name="Precision"
          strokeWidth={2}
          dot={false}
        />
        <Line
          type="monotone"
          dataKey="recall"
          stroke="#f59e0b"
          name="Recall"
          strokeWidth={2}
          dot={false}
        />
        <Line
          type="monotone"
          dataKey="f1_score"
          stroke="#ef4444"
          name="F1 score"
          strokeWidth={2}
          dot={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
