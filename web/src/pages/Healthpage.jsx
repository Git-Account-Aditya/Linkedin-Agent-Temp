import { useEffect, useState } from 'react'
import { api } from '../lib/api'

export default function HealthPage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/health')               // <-- adjust if your backend uses a different path
      .then(res => setData(res.data))
      .catch(err => setError(err?.message || 'Error'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div className="text-red-600">Error: {error}</div>

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-2">Health</h1>
      <pre className="bg-slate-900 text-slate-100 p-3 rounded overflow-auto">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  )
}
