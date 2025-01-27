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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setIsSearching(true)
    // Simulate API call with setTimeout
    setTimeout(() => {
      const mockResults = generateMockResults(company)
      setSearchResults(mockResults)
      setIsSearching(false)
    }, 1500) // Simulate 1.5 second delay
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
            disabled={isSearching}
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
      </div>
      {searchResults.length > 0 && (
        <div className="mt-12 w-full max-w-4xl mx-auto px-4 z-10">
          <ResultsTable company={company} results={searchResults} />
        </div>
      )}
    </div>
  )
}

function generateMockResults(company: string) {
  const positions = ["Software Engineer", "Product Manager", "Data Scientist", "UX Designer", "Marketing Specialist"]
  const results = []
  for (let i = 0; i < 5; i++) {
    results.push({
      name: `Alumni ${i + 1}`,
      position: positions[Math.floor(Math.random() * positions.length)],
      email: `alumni${i + 1}@${company.toLowerCase().replace(/\s+/g, "")}.com`,
    })
  }
  return results
}

