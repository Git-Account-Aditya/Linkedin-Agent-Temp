import { useState } from 'react'
import { api } from '../lib/api'

export default function OrchestratorPage() {
  const [userId, setUserId] = useState('demo-user')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const run = async () => {
    setLoading(true)
    try {
      const data = await api('/api/v1/orchestrator/run', {
        method: 'POST',
        body: JSON.stringify({ user_id: userId }),
      })
      setResult(data)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      <div className="text-sm opacity-80">POST /api/v1/orchestrator/run</div>
      <div className="flex gap-2">
        <input
          className="px-3 py-2 rounded bg-slate-800 border border-slate-700 outline-none w-64"
          value={userId}
          onChange={e => setUserId(e.target.value)}
          placeholder="user id"
        />
        <button
          onClick={run}
          disabled={loading}
          className="px-4 py-2 rounded bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50"
        >
          {loading ? 'Running...' : 'Run'}
        </button>
      </div>
      {result && <pre className="p-4 rounded bg-slate-800">{JSON.stringify(result, null, 2)}</pre>}
    </div>
  )
}