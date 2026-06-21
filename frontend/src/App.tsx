import { useState } from 'react';
import { useChat } from './hooks/useChat';
import { ChatWindow } from './components/ChatWindow';
import { ImagePanel } from './components/ImagePanel';
import { AnalyticsDashboard } from './components/AnalyticsDashboard';
import './index.css';

type Tab = 'chat' | 'analytics';

export default function App() {
  const { messages, isLoading, latestImage, sendMessage, clearSession } = useChat();
  const [tab, setTab] = useState<Tab>('chat');

  return (
    <div className="flex flex-col h-screen bg-[#0f1117]">
      {/* Header */}
      <header className="flex items-center justify-between px-5 py-3 border-b border-slate-800 bg-[#0f1117] flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-base">
            ✈
          </div>
          <div>
            <h1 className="text-white font-semibold text-base leading-none">SkyAssist</h1>
            <p className="text-slate-500 text-xs">AI Airline Support</p>
          </div>
        </div>

        <div className="flex items-center gap-1 bg-slate-800 rounded-lg p-1">
          <button
            onClick={() => setTab('chat')}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
              tab === 'chat'
                ? 'bg-slate-700 text-white'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            💬 Chat
          </button>
          <button
            onClick={() => setTab('analytics')}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
              tab === 'analytics'
                ? 'bg-slate-700 text-white'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            📊 Analytics
          </button>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 overflow-hidden">
        {tab === 'chat' ? (
          <div className="flex h-full">
            {/* Chat panel */}
            <div className="flex-1 flex flex-col border-r border-slate-800 min-w-0">
              <ChatWindow
                messages={messages}
                isLoading={isLoading}
                onSend={sendMessage}
                onClear={clearSession}
              />
            </div>

            {/* Image panel */}
            <div className="w-80 flex-shrink-0 bg-slate-900/50">
              <ImagePanel image_b64={latestImage} />
            </div>
          </div>
        ) : (
          <AnalyticsDashboard />
        )}
      </main>
    </div>
  );
}
