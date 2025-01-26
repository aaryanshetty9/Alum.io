"use client"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function SearchPage() {
  const [company, setCompany] = useState("")
  const [results, setResults] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError("")
    
    try {
      const response = await fetch('http://localhost:5000/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        mode: 'cors',
        body: JSON.stringify({ company }),
      })
      
      if (!response.ok) {
        const errorData = await response.text()
        throw new Error(errorData || 'Search failed')
      }
      
      const data = await response.json()
      setResults(Array.isArray(data) ? data : [])
    } catch (err: any) {
      console.error('Detailed error:', err)
      setError(err.message || 'Failed to search. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto mt-16 px-4">
      <h1 className="text-4xl font-bold mb-8 text-center text-indigo-600">Find Alumni Connections</h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-1">
            Enter Company Name
          </label>
          <Input
            type="text"
            id="company"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            placeholder="e.g. Google, Amazon, Microsoft"
            required
            className="w-full"
          />
        </div>
        <Button
          type="submit"
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white transition-colors duration-300"
          
        >
          Search
        </Button>
      </form>
      
      {isLoading && <p className="mt-4 text-center">Searching...</p>}
      {error && <p className="mt-4 text-center text-red-500">{error}</p>}
      
      {results.length > 0 && (
        <div className="mt-8">
          <h2 className="text-2xl font-bold mb-4">Results</h2>
          <div className="space-y-4">
            {results.map((result, index) => (
              <div key={index} className="p-4 border rounded-lg">
                <h3 className="font-bold">{result.name}</h3>
                <p>{result.role} at {result.company}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

