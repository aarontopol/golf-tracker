import Link from "next/link";

export default function AppHeader({ backLink }: { backLink?: boolean }) {
  return (
    <header className="border-b border-amber-100 bg-white/80 backdrop-blur sticky top-0 z-10">
      <div className="mx-auto flex max-w-5xl items-center gap-3 px-4 py-3 sm:px-6">
        <Link href="/" className="flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-600 text-lg shadow-sm">
            <span aria-hidden>☕</span>
          </span>
          <span>
            <span className="block text-lg font-semibold leading-tight text-slate-900">
              Techie Brekkie
            </span>
            <span className="block text-xs text-slate-500">
              One-hour tax technical sessions
            </span>
          </span>
        </Link>
        {backLink && (
          <Link
            href="/"
            className="ml-auto rounded-lg px-3 py-2 text-sm font-medium text-amber-700 hover:bg-amber-50"
          >
            ← Back to the Box
          </Link>
        )}
      </div>
    </header>
  );
}
