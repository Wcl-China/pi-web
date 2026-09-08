import { toSlashPath } from "./paths";

// In-memory roots that should be browsable in addition to roots derived from
// persisted sessions. Stored on globalThis so Next.js hot-reload keeps them.
declare global {
  var __jiyunAllowedRootsCache: { roots: Set<string>; expiresAt: number } | undefined;
  var __jiyunAdditionalAllowedRoots: Set<string> | undefined;
}

/**
 * Allowed roots are internal bookkeeping keys that are never displayed, so they
 * are stored slash-normalized for consistent Set membership. Correctness does
 * not depend on it — isPathWithinRoots() re-normalizes whatever it is given.
 */
export function normalizeSlashes(filePath: string): string {
  return toSlashPath(filePath);
}

export function getAdditionalAllowedRoots(): Set<string> {
  if (!globalThis.__jiyunAdditionalAllowedRoots) {
    globalThis.__jiyunAdditionalAllowedRoots = new Set();
  }
  return globalThis.__jiyunAdditionalAllowedRoots;
}

export function allowFileRoot(root: string): void {
  if (!root) return;
  const normalizedRoot = normalizeSlashes(root);
  getAdditionalAllowedRoots().add(normalizedRoot);
  globalThis.__jiyunAllowedRootsCache?.roots.add(normalizedRoot);
}
