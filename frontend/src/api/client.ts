import type { ChatMessage, AnalyticsData } from '../types';

const BASE = '';

export async function sendMessage(
  session_id: string,
  message: string
): Promise<Omit<ChatMessage, 'id' | 'role' | 'timestamp'> & { reply: string }> {
  const res = await fetch(`${BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id, message }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function fetchAnalytics(): Promise<AnalyticsData> {
  const res = await fetch(`${BASE}/analytics`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}
