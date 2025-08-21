import axios from 'axios';

const BASE_1 = process.env.CIMEIKA_API_BASE_1;
const BASE_2 = process.env.CIMEIKA_API_BASE_2;

const TIMEOUT_MS = 3000;
const MAX_RETRIES = 3;
const INITIAL_BACKOFF_MS = 100;
export const OFFLINE_MESSAGE = 'Сервіс тимчасово недоступний. Будь ласка, спробуйте пізніше.';

async function requestWithRetry(baseUrl: string | undefined, path: string): Promise<any | null> {
  if (!baseUrl) return null;
  let backoff = INITIAL_BACKOFF_MS;
  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    try {
      const response = await axios.get(`${baseUrl}${path}`, { timeout: TIMEOUT_MS });
      return response.data;
    } catch (error) {
      if (attempt === MAX_RETRIES) break;
      await new Promise((resolve) => setTimeout(resolve, backoff));
      backoff *= 2;
    }
  }
  return null;
}

export async function fetchWithFallback(path: string): Promise<{ data?: any; offline?: boolean; message?: string }> {
  const primary = await requestWithRetry(BASE_1, path);
  if (primary !== null) {
    return { data: primary };
  }
  const fallback = await requestWithRetry(BASE_2, path);
  if (fallback !== null) {
    return { data: fallback };
  }
  return { offline: true, message: OFFLINE_MESSAGE };
}
