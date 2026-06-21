const TOOL_ICONS: Record<string, string> = {
  'get_ticket_price': '🔧',
  'dall-e-3':         '🎨',
  'tts-1':            '🔊',
};

interface Props {
  tools: string[];
}

export function ToolCallIndicator({ tools }: Props) {
  if (!tools || tools.length === 0) return null;
  return (
    <div className="flex flex-wrap gap-1 mt-1">
      {tools.map((tool) => (
        <span
          key={tool}
          className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs bg-amber-500/10 text-amber-300 border border-amber-500/20"
        >
          {TOOL_ICONS[tool] ?? '⚙️'} {tool}
        </span>
      ))}
    </div>
  );
}
