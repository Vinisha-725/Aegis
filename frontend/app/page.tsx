import Link from "next/link"

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-black">
      <div className="text-center space-y-8">
        <h1 className="text-5xl font-bold text-green-400">
          Aegis Protocol
        </h1>
        <p className="text-xl text-gray-400">
          Blockchain Test Console
        </p>
        <Link href="/dashboard">
          <button className="px-8 py-4 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg transition-colors">
            Go to Dashboard
          </button>
        </Link>
      </div>
    </div>
  )
}
