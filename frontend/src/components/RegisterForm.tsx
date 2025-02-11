"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Button } from "@/src/components/ui/button"
import { Input } from "@/src/components/ui/input"
import { Label } from "@/src/components/ui/label"
import { Card, CardContent, CardFooter } from "@/src/components/ui/card"
import {router} from "next/client";

export function RegisterForm() {
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // TODO: Parameterize all base URL
    try {
      const registerResponse = await fetch("http://localhost:8000/users/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password, name }),
      });

      const registerData = await registerResponse.json()

      if (registerResponse.ok) {
        router.push(`/login/?registered=true&email=${encodeURIComponent(registerData.email)}`)
      }
    } catch (error) {
      console.error("Signup error:", error)
    }
  }

  return (
    <Card className="bg-transparent border-green-300">
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4 pt-6">
          <div className="space-y-2">
            <Label htmlFor="name" className="text-green-200">
              Full Name
            </Label>
            <Input
              id="name"
              type="text"
              placeholder="Enter your full name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="bg-white bg-opacity-20 border-green-300 text-green-100 placeholder-green-300"
            />
          </div>
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
              placeholder="Create a password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="bg-white bg-opacity-20 border-green-300 text-green-100 placeholder-green-300"
            />
          </div>
        </CardContent>
        <CardFooter className="flex flex-col space-y-4">
          <Button type="submit" className="w-full bg-green-600 hover:bg-green-700 text-white">
            Create Account
          </Button>
          <p className="text-sm text-green-200">
            Already have an account?{" "}
            <Link href="/frontend/public" className="font-medium text-green-300 hover:text-green-100 transition-colors">
              Sign in
            </Link>
          </p>
        </CardFooter>
      </form>
    </Card>
  )
}

