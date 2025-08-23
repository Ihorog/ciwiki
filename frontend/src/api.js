export async function fetchVoice(voice) {
  try {
    const res = await fetch(`/api/${voice}`);
    if (!res.ok) throw new Error('Network response was not ok');
    return await res.json();
  } catch (err) {
    return { message: `Placeholder response for ${voice}` };
  }
}
