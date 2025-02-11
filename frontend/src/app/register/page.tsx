import { RegisterForm } from "@/src/components/RegisterForm"

export default function Register() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-900 via-green-800 to-green-900">
      <div className="w-full max-w-md p-8 space-y-8 bg-white bg-opacity-10 backdrop-blur-lg rounded-xl shadow-2xl">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-green-100">Narvis</h1>
          <p className="mt-2 text-green-200">Create your account</p>
        </div>
        <RegisterForm />
      </div>
    </main>
  )
}

