jest.mock('axios');
const axios = require('axios');

describe('fetchWithFallback', () => {
  beforeEach(() => {
    axios.get.mockReset();
    try {
      delete require.cache[require.resolve('../src/apiClient')];
    } catch (e) {}
  });

  test('uses primary base when available', async () => {
    process.env.CIMEIKA_API_BASE_1 = 'http://primary';
    process.env.CIMEIKA_API_BASE_2 = 'http://fallback';
    const { fetchWithFallback } = require('../src/apiClient');

    axios.get.mockResolvedValueOnce({ data: { ok: true } });

    const result = await fetchWithFallback('/ping');
    expect(result).toEqual({ data: { ok: true } });
    expect(axios.get).toHaveBeenCalledWith('http://primary/ping', expect.any(Object));
  });

  test('falls back to secondary base after primary failures', async () => {
    process.env.CIMEIKA_API_BASE_1 = 'http://primary';
    process.env.CIMEIKA_API_BASE_2 = 'http://fallback';
    const { fetchWithFallback } = require('../src/apiClient');

    axios.get
      .mockRejectedValueOnce(new Error('fail'))
      .mockRejectedValueOnce(new Error('fail'))
      .mockRejectedValueOnce(new Error('fail'))
      .mockRejectedValueOnce(new Error('fail'))
      .mockResolvedValueOnce({ data: { ok: true } });

    const result = await fetchWithFallback('/ping');
    expect(result).toEqual({ data: { ok: true } });
    expect(axios.get.mock.calls[4][0]).toBe('http://fallback/ping');
  });

  test('returns offline when both bases fail', async () => {
    process.env.CIMEIKA_API_BASE_1 = 'http://primary';
    process.env.CIMEIKA_API_BASE_2 = 'http://fallback';
    const { fetchWithFallback, OFFLINE_MESSAGE } = require('../src/apiClient');

    axios.get
      .mockRejectedValueOnce(new Error('fail'))
      .mockRejectedValueOnce(new Error('fail'))
      .mockRejectedValueOnce(new Error('fail'))
      .mockRejectedValueOnce(new Error('fail'))
      .mockRejectedValueOnce(new Error('fail'))
      .mockRejectedValueOnce(new Error('fail'))
      .mockRejectedValueOnce(new Error('fail'))
      .mockRejectedValueOnce(new Error('fail'));

    const result = await fetchWithFallback('/ping');
    expect(result).toEqual({ offline: true, message: OFFLINE_MESSAGE });
  });
});
