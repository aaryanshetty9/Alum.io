import type React from "react"
import { useState } from "react"
import { Copy, Check } from "lucide-react"
import { Button } from "@/components/ui/button"

interface CopyButtonProps {
  textToCopy: string
}

const CopyButton: React.FC<CopyButtonProps> = ({ textToCopy }) => {
  const [isCopied, setIsCopied] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(textToCopy)
      setIsCopied(true)
      setTimeout(() => setIsCopied(false), 2000)
    } catch (err) {
      console.error("Failed to copy text: ", err)
    }
  }

  return (
    <Button variant="ghost" size="sm" onClick={handleCopy} className="p-1 h-8 w-8">
      {isCopied ? <Check className="h-4 w-4 text-green-500" /> : <Copy className="h-4 w-4" />}
    </Button>
  )
}

export default CopyButton

