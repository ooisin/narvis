import { LoginForm } from "@/src/components/LoginForm"

export default function Home({
  searchParams,
}: {
  searchParams: { registered?: string; email?: string }
}) {
  const justRegistered = searchParams.registered === "true"
  const email = searchParams.email || ""

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-900 via-green-800 to-green-900">
      <div className="w-full max-w-md p-8 space-y-8 bg-white bg-opacity-10 backdrop-blur-lg rounded-xl shadow-2xl">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-green-100">NARVIS</h1>
          <p className="mt-2 text-green-200">Log in to your account</p>
        </div>
        {justRegistered && (
          <div className="bg-red-500 text-white p-4 rounded-md mb-4">
            Registration successful! Please log in with your new account.
          </div>
        )}
        <LoginForm initialEmail={email} />
      </div>
    </main>
  )
}