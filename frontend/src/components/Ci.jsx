import { useEffect, useState } from 'react';
import { fetchVoice } from '../api';

export default function Ci() {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetchVoice('ci').then(setData);
  }, []);
  return (
    <section>
      <h2>Ci</h2>
      <p>{data ? data.message : 'Loading...'}</p>
    </section>
  );
}
