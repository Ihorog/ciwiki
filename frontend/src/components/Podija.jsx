import { useEffect, useState } from 'react';
import { fetchVoice } from '../api';

export default function Podija() {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetchVoice('podija').then(setData);
  }, []);
  return (
    <section>
      <h2>PoDija</h2>
      <p>{data ? data.message : 'Loading...'}</p>
    </section>
  );
}
