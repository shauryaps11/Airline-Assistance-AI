export type Intent =
  | 'price_inquiry'
  | 'destination_image'
  | 'booking_info'
  | 'general_faq'
  | 'escalation';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  intent?: Intent;
  confidence?: number;
  tools_used?: string[];
  escalated?: boolean;
  escalation_summary?: string | null;
  image_b64?: string | null;
  audio_b64?: string | null;
  timestamp: number;
}

export interface AnalyticsData {
  total_sessions: number;
  total_messages: number;
  escalated_count: number;
  resolution_rate: number;
  avg_tools_per_session: number;
  intent_distribution: Record<string, number>;
  escalation_by_trigger: Record<string, number>;
  daily_messages: { day: string; count: number }[];
}
