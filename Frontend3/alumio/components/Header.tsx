import Link from "next/link"

export default function Header() {
  return (
    <header className="bg-white shadow-sm">
      <nav className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <Link href="/" className="text-3xl font-bold text-indigo-600">
            Alum.io
          </Link>
          <div className="h-6 w-px bg-indigo-600"></div>
          <img
            src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-lBqIyArSULr5Kv5WojYL7LpsoLkuBA.png"
            alt="Northeastern University Husky"
            className="h-10 w-auto"
          />
        </div>
        <ul className="flex space-x-4">
          <li>
            <Link href="/" className="text-gray-600 hover:text-indigo-600 transition-colors">
              Home
            </Link>
          </li>
          <li>
            <Link href="/search" className="text-gray-600 hover:text-indigo-600 transition-colors">
              Search
            </Link>
          </li>
        </ul>
      </nav>
    </header>
  )
}

