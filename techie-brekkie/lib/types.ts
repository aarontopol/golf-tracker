export type TopicStatus = "in-box" | "taught";

export interface TopicReference {
  title: string;
  url: string;
  kind?: string; // "code" | "regulation" | "case" | "ruling" | "other"
}

export interface Topic {
  id: string;
  title: string;
  details?: string;
  codeSection?: string; // e.g. "IRC §163(j)" or "s 100A ITAA 1936"
  addedBy?: string;
  createdAt: string; // ISO timestamp
  status: TopicStatus;
  taughtDate?: string; // ISO timestamp — set when the topic is picked & taught
  references?: TopicReference[]; // auto-researched authorities
  referencesStatus?: "pending" | "done" | "failed";
}
