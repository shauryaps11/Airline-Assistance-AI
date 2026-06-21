interface Props {
  summary: string | null;
}

export function EscalationBanner({ summary }: Props) {
  return (
    <div className="mx-4 mb-3 p-3 rounded-lg bg-red-500/10 border border-red-500/30 flex gap-3">
      <span className="text-red-400 text-lg flex-shrink-0">🚨</span>
      <div>
        <p className="text-red-300 font-semibold text-sm mb-0.5">Escalated to Human Agent</p>
        {summary && (
          <p className="text-red-300/80 text-xs leading-relaxed">{summary}</p>
        )}
      </div>
    </div>
  );
}
