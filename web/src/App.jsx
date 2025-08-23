import { Routes, Route, Link } from "react-router-dom"
import { useState } from "react"
import LandingPage from "./pages/LandingPage"

function About() {
  return <h1 className="text-3xl font-bold text-white">About Page</h1>
}

function AutoPosts() {
  return <h1 className="text-3xl font-bold text-white">Auto Generate LinkedIn Posts</h1>
}

function JobTracker() {
  return <h1 className="text-3xl font-bold text-white">Job Tracker</h1>
}

function ProfileAnalyzer() {
  return <h1 className="text-3xl font-bold text-white">Profile Analyzer</h1>
}

function BackendStatus() {
  const [status, setStatus] = useState("Not checked")

  const checkBackend = async () => {
    try {
      const res = await fetch("/api/health")
      const data = await res.json()
      setStatus(`✅ Backend says: ${data.status}`)
    } catch (err) {
      console.error(err)
      setStatus("❌ Cannot reach backend")
    }
  }

  return (
    <div className="mt-6 p-4 bg-white/10 rounded-xl shadow-lg text-white">
      <h2 className="text-xl font-semibold mb-2">Backend Connection Test</h2>
      <button
        onClick={checkBackend}
        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-medium"
      >
        Check Backend
      </button>
      <p className="mt-3">{status}</p>
    </div>
  )
}

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-800 to-red-900 flex flex-col items-center p-6">
      
      {/* NavBar */}
      <div className="rounded-2xl shadow-lg px-8 py-4 flex gap-6 justify-center bg-white">
        <Link to="/" className="text-blue-600 font-medium hover:underline">Home</Link>
        <Link to="/about" className="text-blue-600 font-medium hover:underline">About</Link>
        <Link to="/auto-posts" className="text-blue-600 font-medium hover:underline">Auto Posts</Link>
        <Link to="/job-tracker" className="text-blue-600 font-medium hover:underline">Job Tracker</Link>
        <Link to="/profile-analyzer" className="text-blue-600 font-medium hover:underline">Profile Analyzer</Link>
      </div>

      {/* Routes */}
      <div className="mt-10">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/about" element={<About />} />
          <Route path="/auto-posts" element={<AutoPosts />} />
          <Route path="/job-tracker" element={<JobTracker />} />
          <Route path="/profile-analyzer" element={<ProfileAnalyzer />} />
        </Routes>
      </div>

      {/* Backend check */}
      <BackendStatus />
    </div>
  )
}
