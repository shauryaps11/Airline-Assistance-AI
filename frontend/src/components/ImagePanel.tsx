interface Props {
  image_b64: string | null;
}

export function ImagePanel({ image_b64 }: Props) {
  if (!image_b64) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-slate-500 gap-3">
        <span className="text-5xl">🌍</span>
        <p className="text-sm text-center px-4">
          Ask about a destination to see an AI-generated travel image
        </p>
      </div>
    );
  }

  return (
    <div className="p-3 h-full flex flex-col">
      <p className="text-xs text-slate-400 mb-2 text-center">AI-Generated Destination</p>
      <div className="flex-1 rounded-xl overflow-hidden">
        <img
          src={`data:image/png;base64,${image_b64}`}
          alt="AI-generated destination"
          className="w-full h-full object-cover rounded-xl"
        />
      </div>
      <p className="text-xs text-slate-500 mt-2 text-center">Generated with DALL·E 3</p>
    </div>
  );
}
