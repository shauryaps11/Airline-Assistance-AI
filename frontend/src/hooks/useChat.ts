import { useState, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';
import type { ChatMessage } from '../types';
import { sendMessage as apiSend } from '../api/client';

const SESSION_KEY = 'skyassist_session_id';

function getSessionId(): string {
  let id = localStorage.getItem(SESSION_KEY);
  if (!id) {
    id = uuidv4();
    localStorage.setItem(SESSION_KEY, id);
  }
  return id;
}

export function useChat() {
  const [sessionId] = useState<string>(getSessionId);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [latestImage, setLatestImage] = useState<string | null>(null);

  const sendMessage = useCallback(async (text: string) => {
    const userMsg: ChatMessage = {
      id: uuidv4(),
      role: 'user',
      content: text,
      timestamp: Date.now(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const data = await apiSend(sessionId, text);

      if (data.audio_b64) {
        const audio = new Audio(`data:audio/mpeg;base64,${data.audio_b64}`);
        audio.play().catch(() => {});
      }

      if (data.image_b64) {
        setLatestImage(data.image_b64);
      }

      const assistantMsg: ChatMessage = {
        id: uuidv4(),
        role: 'assistant',
        content: data.reply,
        intent: data.intent as ChatMessage['intent'],
        confidence: data.confidence,
        tools_used: data.tools_used,
        escalated: data.escalated,
        escalation_summary: data.escalation_summary,
        image_b64: data.image_b64,
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      const errMsg: ChatMessage = {
        id: uuidv4(),
        role: 'assistant',
        content: 'Something went wrong. Please try again.',
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId]);

  const clearSession = useCallback(() => {
    setMessages([]);
    setLatestImage(null);
    localStorage.removeItem(SESSION_KEY);
    window.location.reload();
  }, []);

  return { sessionId, messages, isLoading, latestImage, sendMessage, clearSession };
}
