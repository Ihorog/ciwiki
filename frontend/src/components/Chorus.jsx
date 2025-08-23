import { useEffect, useState } from 'react';
import { fetchVoice } from '../api';

const VOICES = ['ci', 'kazkar', 'podija', 'malya', 'nastrij'];

export default function Chorus() {
  const [data, setData] = useState({});
  useEffect(() => {
    Promise.all(
      VOICES.map((v) => fetchVoice(v).then((res) => ({ key: v, value: res })))
    ).then((results) => {
      const map = {};
      results.forEach(({ key, value }) => {
        map[key] = value;
      });
      setData(map);
    });
  }, []);
  return (
    <section>
      <h2>Chorus</h2>
      {VOICES.map((v) => (
        <div key={v}>
          <strong>{v}</strong>: {data[v] ? data[v].message : 'Loading...'}
        </div>
      ))}
    </section>
  );
}
