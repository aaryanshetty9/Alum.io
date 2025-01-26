"use client"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Copy } from "lucide-react"

export default function SearchPage() {
  const [company, setCompany] = useState("")
  const [results, setResults] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")
  const [copiedEmail, setCopiedEmail] = useState<string | null>(null)

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

  const handleCopyEmail = async (email: string) => {
    try {
      await navigator.clipboard.writeText(email)
      setCopiedEmail(email)
      setTimeout(() => setCopiedEmail(null), 2000) // Reset after 2 seconds
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const formatLinkedInUrl = (name: string) => {
    // Convert name to lowercase and replace spaces with hyphens
    const formattedName = name.toLowerCase().replace(/\s+/g, '-');
    return `https://www.linkedin.com/in/${formattedName}`;
  };

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
              <div key={index} className="p-4 border rounded-lg relative">
                <button
                  onClick={() => handleCopyEmail(result.email)}
                  className="absolute top-4 right-4 p-1 hover:bg-gray-100 rounded-full transition-colors"
                  title="Copy email"
                >
                  <Copy size={16} className={copiedEmail === result.email ? "text-green-500" : "text-gray-500"} />
                </button>
                <h3 className="font-bold">
                  <a 
                    href={formatLinkedInUrl(result.name)}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-indigo-600 hover:text-indigo-800 hover:underline"
                  >
                    {result.name}
                  </a>
                </h3>
                <p>{result.email}</p>
                <p>{result.title}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

