"use client"

import { Button } from "@/components/ui/button"
import InteractiveBackground from "@/components/InteractiveBackground"
import { useRef } from "react"
import { SearchSection } from "@/components/SearchSection"
import HowItWorks from "@/components/HowItWorks"
import Footer from "@/components/Footer"
import RotatingCompanies from "@/components/RotatingCompanies"

export default function Home() {
  const searchRef = useRef<HTMLDivElement>(null)

  const scrollToSearch = () => {
    searchRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  return (
    <div className="relative min-h-screen">
      <InteractiveBackground />
      <div className="min-h-screen flex flex-col items-center justify-center">
        <div className="text-center z-10 mb-8">
          <h1 className="text-5xl font-bold mb-6 text-indigo-600">Welcome to Alum.io</h1>
          <p className="text-xl mb-8 max-w-2xl mx-auto text-gray-600">
            Connect with Northeastern alumni and get referrals to your{" "}
            <span className="inline-block animate-pulse text-indigo-600 font-semibold">dream</span> companies.
          </p>
          <Button
            size="lg"
            className="bg-indigo-600 hover:bg-indigo-700 text-white transition-colors duration-300"
            onClick={scrollToSearch}
          >
            Start Your Search
          </Button>
        </div>
        <RotatingCompanies />
      </div>
      <div ref={searchRef}>
        <SearchSection />
      </div>
      <HowItWorks />
      <Footer />
    </div>
  )
}

