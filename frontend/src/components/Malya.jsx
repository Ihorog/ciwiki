import { useEffect, useState } from 'react';
import { fetchVoice } from '../api';

export default function Malya() {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetchVoice('malya').then(setData);
  }, []);
  return (
    <section>
      <h2>Malya</h2>
      <p>{data ? data.message : 'Loading...'}</p>
    </section>
  );
}
