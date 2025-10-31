import { SignedIn, SignedOut } from "@clerk/nextjs";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-16">
            <h1 className="text-5xl font-bold mb-4 text-gray-900">
              Welcome to Movie Store
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              A modern full-stack movie rental application
            </p>
            
            <SignedOut>
              <div className="bg-blue-100 border border-blue-200 rounded-lg p-6 mb-8">
                <p className="text-blue-800 text-lg">
                  👋 Sign in to start browsing and renting movies!
                </p>
              </div>
            </SignedOut>
            
            <SignedIn>
              <div className="bg-green-100 border border-green-200 rounded-lg p-6 mb-8">
                <p className="text-green-800 text-lg">
                  ✅ You&apos;re signed in! Start exploring the movie collection.
                </p>
              </div>
            </SignedIn>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-2 gap-8 mb-16">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-semibold mb-4 text-gray-900">
                🎬 Frontend Features
              </h2>
              <ul className="space-y-2 text-gray-700">
                <li>✓ Next.js 16 with App Router</li>
                <li>✓ Clerk Authentication</li>
                <li>✓ TypeScript & Tailwind CSS</li>
                <li>✓ Modern, responsive UI</li>
              </ul>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-semibold mb-4 text-gray-900">
                ⚙️ Backend Features
              </h2>
              <ul className="space-y-2 text-gray-700">
                <li>✓ Flask REST API</li>
                <li>✓ Movie & category management</li>
                <li>✓ Rental & payment system</li>
                <li>✓ User authentication</li>
              </ul>
            </div>
          </div>

          {/* Tech Stack */}
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-2xl font-semibold mb-6 text-center text-gray-900">
              Technology Stack
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="text-3xl mb-2">⚛️</div>
                <div className="font-medium">Next.js</div>
              </div>
              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="text-3xl mb-2">🐍</div>
                <div className="font-medium">Flask</div>
              </div>
              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="text-3xl mb-2">🔐</div>
                <div className="font-medium">Clerk</div>
              </div>
              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="text-3xl mb-2">🐳</div>
                <div className="font-medium">Docker</div>
              </div>
            </div>
          </div>

          {/* API Info */}
          <div className="mt-8 bg-gray-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-3 text-gray-900">
              Backend API Endpoints
            </h3>
            <div className="text-sm text-gray-600 space-y-1 font-mono">
              <p>• GET /api/v1/movies - List all movies</p>
              <p>• GET /api/v1/movies/search?genre=drama - Search by genre</p>
              <p>• GET /api/v1/categories - List all categories</p>
              <p>• POST /api/v1/rent - Rent a movie</p>
              <p>• GET /api/v1/orders - View your orders</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
