import { Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, Legend, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const colors = ["#FF5A5F", "#FFC857", "#2ECC71", "#38bdf8", "#a78bfa", "#fb7185", "#f97316"];

export function TrendChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <AreaChart data={data}>
        <defs>
          <linearGradient id="trend" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#FF5A5F" stopOpacity={0.8} />
            <stop offset="95%" stopColor="#FF5A5F" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#243B42" />
        <XAxis dataKey="date" stroke="#94A3B8" />
        <YAxis stroke="#94A3B8" />
        <Tooltip contentStyle={{ background: "#10252A", border: "1px solid rgba(255, 90, 95, 0.3)", borderRadius: 14 }} />
        <Area dataKey="stories" stroke="#FF5A5F" fill="url(#trend)" />
      </AreaChart>
    </ResponsiveContainer>
  );
}

export function DonutChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <PieChart>
        <Pie data={data} dataKey="value" nameKey="name" innerRadius={60} outerRadius={95} paddingAngle={4}>
          {data.map((_, index) => <Cell key={index} fill={colors[index % colors.length]} />)}
        </Pie>
        <Tooltip contentStyle={{ background: "#10252A", border: "1px solid rgba(255, 90, 95, 0.3)", borderRadius: 14 }} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}

export function BarMetricChart({ data, xKey, bars }) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#243B42" />
        <XAxis dataKey={xKey} stroke="#94A3B8" />
        <YAxis stroke="#94A3B8" />
        <Tooltip contentStyle={{ background: "#10252A", border: "1px solid rgba(255, 90, 95, 0.3)", borderRadius: 14 }} />
        <Legend />
        {bars.map((bar, index) => <Bar key={bar.key} dataKey={bar.key} name={bar.name} fill={colors[index % colors.length]} radius={[10, 10, 0, 0]} />)}
      </BarChart>
    </ResponsiveContainer>
  );
}

export function LineMetricChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#243B42" />
        <XAxis dataKey="model" stroke="#94A3B8" />
        <YAxis stroke="#94A3B8" />
        <Tooltip contentStyle={{ background: "#10252A", border: "1px solid rgba(255, 90, 95, 0.3)", borderRadius: 14 }} />
        <Line type="monotone" dataKey="avg_generation_time" stroke="#FFC857" strokeWidth={3} />
        <Line type="monotone" dataKey="avg_word_count" stroke="#FF5A5F" strokeWidth={3} />
      </LineChart>
    </ResponsiveContainer>
  );
}
