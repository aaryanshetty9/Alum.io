"use client"

import { useState, useEffect } from "react"
import type React from "react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import CopyButton from "@/components/CopyButton"
import { motion, AnimatePresence } from "framer-motion"

interface Result {
  name: string
  position: string
  email: string
}

interface ResultsTableProps {
  company: string
  results: Result[]
}

const ResultsTable: React.FC<ResultsTableProps> = ({ company, results }) => {
  const [visibleResults, setVisibleResults] = useState<Result[]>([])

  useEffect(() => {
    setVisibleResults([]) // Reset when new results come in
    const timeouts: NodeJS.Timeout[] = []

    // Add each result with a delay
    results.forEach((result, index) => {
      const timeout = setTimeout(() => {
        setVisibleResults(prev => {
          // Check if this result is already in the array
          if (prev.some(r => r.name === result.name && r.email === result.email)) {
            return prev
          }
          return [...prev, result]
        })
      }, index * 750)
      
      timeouts.push(timeout)
    })

    // Cleanup function to clear all timeouts
    return () => {
      timeouts.forEach(timeout => clearTimeout(timeout))
    }
  }, [results])

  return (
    <div className="bg-white shadow-md rounded-lg overflow-hidden">
      <h3 className="text-2xl font-semibold p-4 bg-indigo-600 text-white text-center">{company} Alumni</h3>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>Position</TableHead>
            <TableHead>Email</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <AnimatePresence>
            {visibleResults.map((result, index) => (
              <motion.tr
                key={`${result.name}-${result.email}`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="border-b transition-colors hover:bg-gray-100"
              >
                <TableCell className="font-medium">{result.name}</TableCell>
                <TableCell>{result.position}</TableCell>
                <TableCell className="flex items-center justify-between">
                  <span>{result.email}</span>
                  <CopyButton textToCopy={result.email} />
                </TableCell>
              </motion.tr>
            ))}
          </AnimatePresence>
        </TableBody>
      </Table>
    </div>
  )
}

export default ResultsTable

