import Link from "next/link"

export default function Header() {
  return (
    <header className="bg-white shadow-sm">
      <nav className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-indigo-600">
          Alum.io
        </Link>
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

