import './App.css'
import { Routes, Route } from 'react-router-dom'
import Home from './components/Home'
import Quiz from './components/Quiz'

function App() {
  return (
    <div>
      <Routes>
        <Route
          path="/"
          element={
            <Home />
          }
        />
        <Route
          path="/quiz"
          element={
            <Quiz/>
          }
        />
      </Routes>
    </div>
  )
}

export default App
