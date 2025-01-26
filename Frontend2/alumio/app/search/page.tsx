"use client"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function SearchPage() {
  const [company, setCompany] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Here you would typically handle the search logic
    console.log("Searching for:", company)
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
    </div>
  )
}

