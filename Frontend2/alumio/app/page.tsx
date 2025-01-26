import Link from "next/link"
import { Button } from "@/components/ui/button"
import InteractiveBackground from "@/components/InteractiveBackground"

export default function Home() {
  return (
    <div className="relative min-h-screen flex items-center justify-center">
      <InteractiveBackground />
      <div className="text-center z-10">
        <h1 className="text-5xl font-bold mb-6 text-indigo-600">Welcome to Alum.io</h1>
        <p className="text-xl mb-8 max-w-2xl mx-auto text-gray-600">
          Connect with Northeastern alumni and get referrals to your dream companies.
        </p>
        <Link href="/search">
          <Button size="lg" className="bg-indigo-600 hover:bg-indigo-700 text-white transition-colors duration-300">
            Start Your Search
          </Button>
        </Link>
      </div>
    </div>
  )
}

