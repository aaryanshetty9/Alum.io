"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"

interface Company {
  name: string
  logo: string
}

const companies: Company[] = [
  { name: "Amazon", logo: "https://logo.clearbit.com/amazon.com" },
  { name: "Citadel", logo: "https://logo.clearbit.com/citadel.com" },
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

const RotatingCompanies: React.FC = () => {
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % companies.length)
    }, 4000) // Change company every 4 seconds

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="text-center py-8">
      <h2 className="text-2xl font-bold mb-4 text-indigo-600">Connect with Northeastern Alum @</h2>
      <div className="h-16 flex items-center justify-center">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentIndex}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5 }}
            className="flex items-center space-x-2"
          >
            <img
              src={companies[currentIndex].logo || "/placeholder.svg"}
              alt={companies[currentIndex].name}
              className="w-8 h-8 object-contain"
            />
            <span className="text-xl font-semibold text-gray-800">{companies[currentIndex].name}</span>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  )
}

export default RotatingCompanies

