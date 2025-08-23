import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Ci from './components/Ci';
import Kazkar from './components/Kazkar';
import Podija from './components/Podija';
import Malya from './components/Malya';
import Nastrij from './components/Nastrij';
import Chorus from './components/Chorus';
import './App.css';

function App() {
  return (
    <Router>
      <nav>
        <Link to="/ci">Ci</Link> |{' '}
        <Link to="/kazkar">Kazkar</Link> |{' '}
        <Link to="/podija">PoDija</Link> |{' '}
        <Link to="/malya">Malya</Link> |{' '}
        <Link to="/nastrij">Nastrij</Link> |{' '}
        <Link to="/chorus">Chorus</Link>
      </nav>
      <img src="/media/logo.svg" alt="logo" width="80" />
      <Routes>
        <Route path="/ci" element={<Ci />} />
        <Route path="/kazkar" element={<Kazkar />} />
        <Route path="/podija" element={<Podija />} />
        <Route path="/malya" element={<Malya />} />
        <Route path="/nastrij" element={<Nastrij />} />
        <Route path="/chorus" element={<Chorus />} />
        <Route path="/" element={<Chorus />} />
      </Routes>
    </Router>
  );
}

export default App;
