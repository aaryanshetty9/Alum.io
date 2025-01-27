import { useState, useEffect } from "react"

const companies = ["Amazon", "Google", "Chewy", "Truveta", "Nutiverse", "Lumen", "Ripple", "T-Mobile", "Chime", "Sofi"]

export function useRotatingPlaceholder() {
  const [placeholderIndex, setPlaceholderIndex] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setPlaceholderIndex((prevIndex) => (prevIndex + 1) % companies.length)
    }, 3000) // Change every 3 seconds

    return () => clearInterval(interval)
  }, [])

  return `Ex: ${companies[placeholderIndex]}`
}

