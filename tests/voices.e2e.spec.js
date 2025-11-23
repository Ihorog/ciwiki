import { test, expect } from '@playwright/test';
import { fetchVoice } from '../frontend/src/api.js';

const VOICES = ['ci', 'kazkar', 'podija', 'malya', 'nastrij'];

test('all voices respond', async () => {
  for (const v of VOICES) {
    const res = await fetchVoice(v, 'hello');
    expect(res.message).toContain('Placeholder response');
  }
});
