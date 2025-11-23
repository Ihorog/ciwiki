export async function fetchVoice(voice, prompt = '') {
  try {
    const res = await fetch(`/api/${voice}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });
    if (!res.ok) throw new Error('Network response was not ok');
    return await res.json();
  } catch (err) {
    return { message: `Placeholder response for ${voice}: ${prompt}` };
  }
}
