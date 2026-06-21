import { useEffect, useState } from 'react';
import { fetchAnalytics } from '../api/client';
import type { AnalyticsData } from '../types';

function StatCard({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-4">
      <p className="text-xs text-slate-400 mb-1">{label}</p>
      <p className="text-2xl font-bold text-white">{value}</p>
      {sub && <p className="text-xs text-slate-500 mt-0.5">{sub}</p>}
    </div>
  );
}

const INTENT_COLORS: Record<string, string> = {
  price_inquiry:     'bg-blue-500',
  destination_image: 'bg-purple-500',
  booking_info:      'bg-emerald-500',
  general_faq:       'bg-slate-500',
  escalation:        'bg-red-500',
};

export function AnalyticsDashboard() {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [error, setError] = useState(false);

  const load = async () => {
    try {
      const d = await fetchAnalytics();
      setData(d);
      setError(false);
    } catch {
      setError(true);
    }
  };

  useEffect(() => {
    load();
    const t = setInterval(load, 30_000);
    return () => clearInterval(t);
  }, []);

  if (error) return (
    <div className="p-4 text-center text-slate-500 text-sm">Analytics unavailable</div>
  );
  if (!data) return (
    <div className="p-4 text-center text-slate-500 text-sm animate-pulse">Loading analytics…</div>
  );

  const totalIntents = Object.values(data.intent_distribution).reduce((a, b) => a + b, 0);

  return (
    <div className="p-4 space-y-4 overflow-y-auto h-full">
      <h3 className="text-sm font-semibold text-slate-300 flex items-center gap-2">
        <span>📊</span> Session Analytics
        <span className="ml-auto text-xs text-slate-500 font-normal">auto-refreshes 30s</span>
      </h3>

      <div className="grid grid-cols-2 gap-3">
        <StatCard
          label="Resolution Rate"
          value={`${(data.resolution_rate * 100).toFixed(1)}%`}
          sub="autonomous resolutions"
        />
        <StatCard
          label="Total Sessions"
          value={String(data.total_sessions)}
          sub={`${data.total_messages} messages`}
        />
        <StatCard
          label="Avg Tools / Session"
          value={String(data.avg_tools_per_session)}
          sub="tool calls"
        />
        <StatCard
          label="Escalations"
          value={String(data.escalated_count)}
          sub={`${((data.escalated_count / Math.max(data.total_messages, 1)) * 100).toFixed(1)}% rate`}
        />
      </div>

      {totalIntents > 0 && (
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-3">Intent Distribution</p>
          <div className="space-y-2">
            {Object.entries(data.intent_distribution).map(([intent, count]) => {
              const pct = Math.round((count / totalIntents) * 100);
              return (
                <div key={intent}>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-300">{intent.replace('_', ' ')}</span>
                    <span className="text-slate-400">{count} ({pct}%)</span>
                  </div>
                  <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${INTENT_COLORS[intent] ?? 'bg-slate-500'}`}
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {Object.keys(data.escalation_by_trigger).length > 0 && (
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-2">Escalation Triggers</p>
          <div className="space-y-1">
            {Object.entries(data.escalation_by_trigger).map(([trigger, count]) => (
              <div key={trigger} className="flex justify-between text-xs">
                <span className="text-slate-300">{trigger.replace('_', ' ')}</span>
                <span className="text-red-400 font-medium">{count}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
