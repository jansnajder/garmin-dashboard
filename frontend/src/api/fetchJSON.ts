/** Thrown by fetchJSON on a non-2xx response; carries the HTTP status for callers that need to branch on it (e.g. 401). */
export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

/**
 * Fetch a URL and parse the response body as JSON.
 *
 * @param url - request URL, relative paths work through both the Vite dev proxy and FastAPI's own serving
 * @param init - forwarded to fetch()
 * @returns parsed JSON body
 * @throws {ApiError} on a non-2xx response
 */
export async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
  const resp = await fetch(url, init);

  if (!resp.ok) {
    const text = await resp.text();

    throw new ApiError(resp.status, extractMessage(text) ?? `${resp.status}: ${text}`);
  }

  return resp.json() as Promise<T>;
}

/**
 * Pull FastAPI's `detail` field out of a JSON error body.
 *
 * @param text - raw response body
 * @returns the detail message, or null when the body isn't JSON with a string `detail`
 */
function extractMessage(text: string): string | null {
  try {
    const body = JSON.parse(text);

    return typeof body.detail === 'string' ? body.detail : null;
  } catch {
    return null;
  }
}
