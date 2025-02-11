"use client"

import { useState, useEffect } from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/src/components/ui/card"
import { Button } from "@/src/components/ui/button"
import { PlusCircle } from "lucide-react"

interface Narrative {
  id: string
  title: string
  description: string
}

export function NarrativeTiles() {
  const [narratives, setNarratives] = useState<Narrative[]>([])

  useEffect(() => {
    // In a real application, you would fetch the narratives from an API
    const fetchNarratives = async () => {
      // Simulating an API call with mock data
      const mockNarratives: Narrative[] = [
        { id: "1", title: "New York Stories", description: "A collection of tales from the Big Apple" },
        { id: "2", title: "Paris Nights", description: "Exploring the City of Light after dark" },
        { id: "3", title: "Tokyo Adventures", description: "Navigating the bustling streets of Tokyo" },
      ]
      setNarratives(mockNarratives)
    }

    fetchNarratives()
  }, [])

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {narratives.map((narrative) => (
          <Card key={narrative.id} className="bg-green-700 text-green-100 hover:bg-green-600 transition-colors">
            <CardHeader>
              <CardTitle>{narrative.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p>{narrative.description}</p>
            </CardContent>
          </Card>
        ))}
        <Card className="bg-green-700 text-green-100 hover:bg-green-600 transition-colors flex items-center justify-center cursor-pointer">
          <CardContent>
            <Button variant="ghost" className="w-full h-full flex flex-col items-center justify-center">
              <PlusCircle className="h-12 w-12 mb-2" />
              <span>Create New Narrative</span>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

