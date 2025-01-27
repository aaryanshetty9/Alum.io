import type React from "react"
import { Search, Users, Send } from "lucide-react"

const steps = [
  {
    icon: <Search className="w-12 h-12 text-indigo-600" />,
    title: "Search",
    description: "Enter the name of the company you're interested in.",
  },
  {
    icon: <Users className="w-12 h-12 text-indigo-600" />,
    title: "Connect",
    description: "Find Northeastern alumni working at your desired company.",
  },
  {
    icon: <Send className="w-12 h-12 text-indigo-600" />,
    title: "Reach Out",
    description: "Contact alumni for referrals and career advice.",
  },
]

const HowItWorks: React.FC = () => {
  return (
    <div className="bg-gray-50 py-16">
      <div className="max-w-4xl mx-auto px-4">
        <h2 className="text-3xl font-semibold text-center mb-12 text-gray-800">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((step, index) => (
            <div key={index} className="flex flex-col items-center text-center">
              <div className="mb-4">{step.icon}</div>
              <h3 className="text-xl font-semibold mb-2 text-gray-800">{step.title}</h3>
              <p className="text-gray-600">{step.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default HowItWorks

