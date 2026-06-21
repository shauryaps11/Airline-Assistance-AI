import type { ChatMessage } from '../types';
import { IntentBadge } from './IntentBadge';
import { ToolCallIndicator } from './ToolCallIndicator';

interface Props {
  message: ChatMessage;
}

export function MessageBubble({ message }: Props) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3 px-4`}>
      <div className={`max-w-[80%] ${isUser ? 'items-end' : 'items-start'} flex flex-col gap-1`}>
        {!isUser && (
          <div className="flex items-center gap-2 mb-0.5">
            <div className="w-6 h-6 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-xs">
              ✈
            </div>
            <span className="text-xs text-slate-400">SkyAssist</span>
          </div>
        )}

        <div
          className={`px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
            isUser
              ? 'bg-indigo-600 text-white rounded-tr-sm'
              : 'bg-slate-800 text-slate-100 rounded-tl-sm border border-slate-700'
          }`}
        >
          {message.content}
        </div>

        {!isUser && (
          <div className="flex flex-wrap items-center gap-2 mt-0.5">
            {message.intent && <IntentBadge intent={message.intent} />}
            {message.tools_used && message.tools_used.length > 0 && (
              <ToolCallIndicator tools={message.tools_used} />
            )}
          </div>
        )}
      </div>
    </div>
  );
}
