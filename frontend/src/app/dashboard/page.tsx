import { DashboardHeader } from "@/src/components/DashboardHeader"
import { NarrativeTiles } from "@/src/components/NarrativeTiles"

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-900 via-green-800 to-green-900">
      <DashboardHeader />
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-green-100 mb-6">Your City Narratives</h1>
        <NarrativeTiles />
      </main>
    </div>
  )
}

