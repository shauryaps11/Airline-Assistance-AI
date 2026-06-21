import type { Intent } from '../types';

const INTENT_CONFIG: Record<Intent, { label: string; className: string }> = {
  price_inquiry:     { label: '💰 Price Inquiry',      className: 'bg-blue-500/20 text-blue-300 border-blue-500/30' },
  destination_image: { label: '🌍 Destination',        className: 'bg-purple-500/20 text-purple-300 border-purple-500/30' },
  booking_info:      { label: '🎫 Booking Info',       className: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' },
  general_faq:       { label: '❓ General FAQ',        className: 'bg-slate-500/20 text-slate-300 border-slate-500/30' },
  escalation:        { label: '🚨 Escalated',          className: 'bg-red-500/20 text-red-300 border-red-500/30' },
};

interface Props {
  intent: Intent;
}

export function IntentBadge({ intent }: Props) {
  const cfg = INTENT_CONFIG[intent] ?? { label: intent, className: 'bg-slate-500/20 text-slate-300 border-slate-500/30' };
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${cfg.className}`}>
      {cfg.label}
    </span>
  );
}
