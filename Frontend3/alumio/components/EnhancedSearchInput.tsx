"use client"

import { useState, useEffect, useRef } from "react"
import { Input } from "@/components/ui/input"
import { useRotatingPlaceholder } from "@/hooks/useRotatingPlaceholder"
import styles from "@/styles/RotatingPlaceholder.module.css"

interface Company {
  name: string
  logo: string
}

const companies: Company[] = [
  { name: "Amazon", logo: "https://logo.clearbit.com/amazon.com" },
  { name: "Google", logo: "https://logo.clearbit.com/google.com" },
  { name: "Chewy", logo: "https://logo.clearbit.com/chewy.com" },
  { name: "Truveta", logo: "https://logo.clearbit.com/truveta.com" },
  { name: "Nutiverse", logo: "https://logo.clearbit.com/nutiverse.com" },
  { name: "Lumen", logo: "https://logo.clearbit.com/lumen.com" },
  { name: "Ripple", logo: "https://logo.clearbit.com/ripple.com" },
  { name: "T-Mobile", logo: "https://logo.clearbit.com/t-mobile.com" },
  { name: "Chime", logo: "https://logo.clearbit.com/chime.com" },
  { name: "Sofi", logo: "https://logo.clearbit.com/sofi.com" },
  { name: "Meta", logo: "https://logo.clearbit.com/meta.com" },
]

interface EnhancedSearchInputProps {
  onCompanySelect: (company: string) => void
}

export function EnhancedSearchInput({ onCompanySelect }: EnhancedSearchInputProps) {
  const [query, setQuery] = useState("")
  const [suggestions, setSuggestions] = useState<Company[]>([])
  const [isOpen, setIsOpen] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)
  const suggestionsRef = useRef<HTMLDivElement>(null)
  const placeholder = useRotatingPlaceholder()

  useEffect(() => {
    const filteredCompanies = companies.filter((company) => company.name.toLowerCase().includes(query.toLowerCase()))
    setSuggestions(filteredCompanies)
    setIsOpen(filteredCompanies.length > 0 && query.length > 0)
  }, [query])

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        suggestionsRef.current &&
        !suggestionsRef.current.contains(event.target as Node) &&
        inputRef.current &&
        !inputRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
    }
  }, [])

  const handleSelect = (company: string) => {
    setQuery(company)
    onCompanySelect(company)
    setIsOpen(false)
  }

  return (
    <div className="relative">
      <Input
        ref={inputRef}
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={placeholder}
        className={`w-full ${styles.rotatingPlaceholder}`}
      />
      {isOpen && (
        <div
          ref={suggestionsRef}
          className="absolute z-10 w-full mt-1 bg-white rounded-md shadow-lg max-h-60 overflow-auto"
        >
          {suggestions.map((company) => (
            <div
              key={company.name}
              className="flex items-center p-2 hover:bg-gray-100 cursor-pointer"
              onClick={() => handleSelect(company.name)}
            >
              <img src={company.logo || "/placeholder.svg"} alt={company.name} className="w-6 h-6 mr-2" />
              <span>{company.name}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

