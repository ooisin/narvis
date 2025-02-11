import Link from "next/link"
import { Button } from "@/src/components/ui/button"

export function DashboardHeader() {
  return (
    <header className="bg-green-800 shadow-md">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/dashboard" className="text-2xl font-bold text-green-100">
          Narvis
        </Link>
        <nav>
          <Button variant="ghost" className="text-green-100 hover:text-white hover:bg-green-700">
            Log out
          </Button>
        </nav>
      </div>
    </header>
  )
}

