"use client"

import {useEffect, useState} from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Button } from "@/src/components/ui/button"
import { Input } from "@/src/components/ui/input"
import { Label } from "@/src/components/ui/label"
import { Card, CardContent, CardFooter } from "@/src/components/ui/card"

interface LoginFormProps {
  initialEmail?: string
}

export function LoginForm({ initialEmail = ""}: LoginFormProps) {
  const [email, setEmail] = useState(initialEmail)
  const [password, setPassword] = useState("")
  const router = useRouter()

  useEffect(() => {
  setEmail(initialEmail)
  }, [initialEmail])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // TODO: Parameterize all base URL
    try {
      const response = await fetch("http://localhost:8000/login/access-token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });

      const data = await response.json()

      // TODO: Add pop up for when it fails login for some reason with toast
      if (response.ok) {
        // TODO: Make more secure using Redis etc...
        localStorage.setItem("token", data.access_token)
        router.push("/dashboard")
      }

    } catch (error) {
      console.error("Login error:", error)
    }
  }

     return (
    <Card className="bg-transparent border-green-300">
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4 pt-6">
          <div className="space-y-2">
            <Label htmlFor="email" className="text-green-200">
              Email address
            </Label>
            <Input
              id="email"
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="bg-white bg-opacity-20 border-green-300 text-green-100 placeholder-green-300"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password" className="text-green-200">
              Password
            </Label>
            <Input
              id="password"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="bg-white bg-opacity-20 border-green-300 text-green-100 placeholder-green-300"
            />
          </div>
        </CardContent>
        <CardFooter className="flex flex-col space-y-4">
          <Button type="submit" className="w-full bg-green-600 hover:bg-green-700 text-white">
            Sign in
          </Button>
          <p className="text-sm text-green-200">
            New to Narvis?{" "}
            <Link href="/register" className="font-medium text-green-300 hover:text-green-100 transition-colors">
              Create an account
            </Link>
          </p>
        </CardFooter>
      </form>
    </Card>
  )
}