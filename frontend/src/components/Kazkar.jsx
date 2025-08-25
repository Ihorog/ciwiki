import { useEffect, useState } from 'react';
import { fetchVoice } from '../api';

export default function Kazkar() {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetchVoice('kazkar').then(setData);
  }, []);
  return (
    <section>
      <h2>Kazkar</h2>
      <p>{data ? data.message : 'Loading...'}</p>
    </section>
  );
}
