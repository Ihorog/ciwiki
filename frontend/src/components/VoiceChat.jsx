import { useState } from 'react';
import { fetchVoice } from '../api';
import knowledge from '../knowledge.index.json';

export default function VoiceChat({ voice, title }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    const prompt = input;
    setInput('');
    setMessages((prev) => [...prev, { from: 'user', text: prompt }]);
    const res = await fetchVoice(voice, prompt);
    setMessages((prev) => [...prev, { from: voice, text: res.message }]);
  };

  const suggestions = knowledge.filter(
    (k) => input && k.title.toLowerCase().includes(input.toLowerCase())
  );

  return (
    <section>
      <h2>{title}</h2>
      <ul>
        {messages.map((m, idx) => (
          <li key={idx} data-from={m.from}>
            <strong>[{m.from}]</strong> {m.text}
          </li>
        ))}
      </ul>
      <form onSubmit={sendMessage}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={`Ask ${title}`}
        />
        <button type="submit">Send</button>
      </form>
      {suggestions.length > 0 && (
        <ul>
          {suggestions.map((s) => (
            <li key={s.id}>{s.title}</li>
          ))}
        </ul>
      )}
    </section>
  );
}

