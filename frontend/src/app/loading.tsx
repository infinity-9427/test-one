export default function Loading() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
      <div className="text-center">
        {/* Loading Spinner */}
        <div className="mb-8">
          <div className="relative">
            <div className="w-20 h-20 border-4 border-blue-200 dark:border-blue-800 rounded-full animate-spin border-t-blue-600 dark:border-t-blue-400 mx-auto"></div>
            <div className="absolute inset-0 w-20 h-20 border-4 border-transparent border-t-blue-300 dark:border-t-blue-500 rounded-full animate-spin mx-auto" style={{ animationDelay: '0.3s', animationDuration: '1.5s' }}></div>
          </div>
        </div>

        {/* Loading Text */}
        <div className="space-y-4">
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
            Loading Design Scoring Tool
          </h2>
          <p className="text-gray-600 dark:text-gray-400 max-w-md mx-auto">
            Preparing your website analysis environment...
          </p>
        </div>

        {/* Loading Steps */}
        <div className="mt-8 space-y-2">
          <div className="flex items-center justify-center gap-2 text-sm text-gray-500 dark:text-gray-400">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
            <span>Initializing AI analysis engine</span>
          </div>
          <div className="flex items-center justify-center gap-2 text-sm text-gray-500 dark:text-gray-400">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" style={{ animationDelay: '0.5s' }}></div>
            <span>Setting up report generation</span>
          </div>
          <div className="flex items-center justify-center gap-2 text-sm text-gray-500 dark:text-gray-400">
            <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse" style={{ animationDelay: '1s' }}></div>
            <span>Loading user interface</span>
          </div>
        </div>
      </div>
    </div>
  );
}
