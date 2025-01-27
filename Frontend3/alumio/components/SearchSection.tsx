"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import SubtleBackground from "@/components/SubtleBackground"
import ResultsTable from "@/components/ResultsTable"
import { Send } from "lucide-react"
import { EnhancedSearchInput } from "@/components/EnhancedSearchInput"

export function SearchSection() {
  const [company, setCompany] = useState("")
  const [isSearching, setIsSearching] = useState(false)
  const [searchResults, setSearchResults] = useState<Array<{ name: string; position: string; email: string }>>([])
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!company) return

    setIsSearching(true)
    setError(null)
    
    try {
      const response = await fetch('http://localhost:5000/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ company }),
      })

      if (!response.ok) {
        throw new Error('Failed to fetch results')
      }

      const data = await response.json()
      
      // Transform the data to match our expected format
      const formattedResults = data.map((item: any) => ({
        name: item.name,
        position: item.title,
        email: item.email,
      }))

      setSearchResults(formattedResults)
    } catch (err) {
      setError('Failed to fetch results. Please try again.')
      console.error('Search error:', err)
    } finally {
      setIsSearching(false)
    }
  }

  const handleCompanySelect = (selectedCompany: string) => {
    setCompany(selectedCompany)
  }

  return (
    <div className="relative min-h-screen flex flex-col items-center justify-start pt-20">
      <SubtleBackground />
      <div className="max-w-2xl mx-auto px-4 z-10 w-full">
        <h2 className="text-4xl font-bold mb-8 text-center text-indigo-600">Find Alumni Connections</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-1">
              Enter Company Name
            </label>
            <EnhancedSearchInput onCompanySelect={handleCompanySelect} />
          </div>
          <Button
            type="submit"
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white transition-colors duration-300 flex items-center justify-center"
            disabled={isSearching || !company}
          >
            {isSearching ? (
              "Searching..."
            ) : (
              <>
                <span className="mr-2">Search</span>
                <Send size={16} />
              </>
            )}
          </Button>
        </form>
        {error && (
          <div className="mt-4 p-4 bg-red-50 text-red-600 rounded-md">
            {error}
          </div>
        )}
      </div>
      {searchResults.length > 0 && (
        <div className="mt-12 w-full max-w-4xl mx-auto px-4 z-10">
          <ResultsTable company={company} results={searchResults} />
        </div>
      )}
    </div>
  )
}

