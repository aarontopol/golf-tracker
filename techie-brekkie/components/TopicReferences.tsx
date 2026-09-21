import type { Topic } from "@/lib/types";

const KIND_LABELS: Record<string, string> = {
  code: "Statute",
  regulation: "Regulation",
  case: "Case",
  ruling: "Ruling",
};

export default function TopicReferences({ topic }: { topic: Topic }) {
  if (topic.referencesStatus === "pending") {
    return (
      <p className="mt-2 flex items-center gap-1.5 text-xs text-slate-500">
        <span className="inline-block h-3 w-3 animate-spin rounded-full border-2 border-amber-500 border-t-transparent" />
        Finding the relevant code sections, regulations &amp; cases…
      </p>
    );
  }

  if (!topic.references || topic.references.length === 0) return null;

  return (
    <div className="mt-2.5 flex flex-wrap gap-1.5">
      {topic.references.map((ref) => (
        <a
          key={ref.url}
          href={ref.url}
          target="_blank"
          rel="noopener noreferrer"
          title={ref.title}
          className="inline-flex max-w-full items-center gap-1 rounded-lg border border-sky-200 bg-sky-50 px-2 py-1 text-xs font-medium text-sky-800 transition hover:border-sky-400 hover:bg-sky-100"
        >
          <span aria-hidden>🔗</span>
          {ref.kind && KIND_LABELS[ref.kind] && (
            <span className="rounded bg-sky-200/70 px-1 text-[10px] uppercase tracking-wide">
              {KIND_LABELS[ref.kind]}
            </span>
          )}
          <span className="truncate">{ref.title}</span>
        </a>
      ))}
    </div>
  );
}
