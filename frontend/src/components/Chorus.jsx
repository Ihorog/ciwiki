import { useState } from 'react';
import { fetchVoice } from '../api';
import knowledge from '../knowledge.index.json';

const VOICES = ['ci', 'kazkar', 'podija', 'malya', 'nastrij'];

export default function Chorus() {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState(() => {
    const init = {};
    VOICES.forEach((v) => (init[v] = []));
    return init;
  });

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    const prompt = input;
    setInput('');
    setHistory((prev) => {
      const updated = { ...prev };
      VOICES.forEach((v) => {
        updated[v] = [...updated[v], { from: 'user', text: prompt }];
      });
      return updated;
    });
    const responses = await Promise.all(
      VOICES.map((v) => fetchVoice(v, prompt).then((res) => ({ v, res })))
    );
    setHistory((prev) => {
      const updated = { ...prev };
      responses.forEach(({ v, res }) => {
        updated[v] = [...updated[v], { from: v, text: res.message }];
      });
      return updated;
    });
  };

  const suggestions = knowledge.filter(
    (k) => input && k.title.toLowerCase().includes(input.toLowerCase())
  );

  return (
    <section>
      <h2>Chorus</h2>
      <form onSubmit={sendMessage}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask all voices"
          data-test="chorus-input"
        />
        <button type="submit" data-test="chorus-send">
          Send
        </button>
      </form>
      {suggestions.length > 0 && (
        <ul data-test="suggestions">
          {suggestions.map((s) => (
            <li key={s.id}>{s.title}</li>
          ))}
        </ul>
      )}
      {VOICES.map((v) => (
        <div key={v} data-voice={v}>
          <h3>{v}</h3>
          <ul>
            {history[v].map((m, idx) => (
              <li key={idx} data-from={m.from}>
                <strong>[{m.from}]</strong> {m.text}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </section>
  );
}
