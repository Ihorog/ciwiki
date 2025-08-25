import { useEffect, useState } from 'react';
import { fetchVoice } from '../api';

export default function Nastrij() {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetchVoice('nastrij').then(setData);
  }, []);
  return (
    <section>
      <h2>Nastrij</h2>
      <p>{data ? data.message : 'Loading...'}</p>
    </section>
  );
}
