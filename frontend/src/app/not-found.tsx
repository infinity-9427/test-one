'use client'

import Link from 'next/link';
import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';

export default function NotFound() {
  return (
    <div className="h-screen w-full bg-gradient-to-br from-gray-50 to-blue-50 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4 sm:p-6 lg:p-8">
      <div className="w-full max-w-lg sm:max-w-xl lg:max-w-2xl mx-auto">
        <Card className="shadow-xl border-0 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm w-full">
          <CardContent className="p-6 sm:p-8 md:p-10 lg:p-12 text-center">
            {/* 404 Image */}
            <div className="mb-6 sm:mb-8">
              <Image
                src="/404.webp"
                alt="404 - Page Not Found"
                width={400}
                height={300}
                className="mx-auto rounded-lg shadow-lg w-full max-w-xs sm:max-w-sm md:max-w-md h-auto"
                priority
                unoptimized
              />
            </div>

            {/* Error Content */}
            <div className="space-y-4 sm:space-y-6">
              <div>
                <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-2">
                  404
                </h1>
                <h2 className="text-lg sm:text-xl md:text-2xl font-semibold text-gray-700 dark:text-gray-300 mb-3 sm:mb-4">
                  Page Not Found
                </h2>
                <p className="text-sm sm:text-base md:text-lg text-gray-600 dark:text-gray-400 max-w-sm sm:max-w-md mx-auto leading-relaxed px-2">
                  Oops! The page you&apos;re looking for doesn&apos;t exist. It might have been moved, deleted, or you entered the wrong URL.
                </p>
              </div>

              {/* Action Button */}
              <div className="pt-4 sm:pt-6">
                <Link href="/">
                  <Button size="lg" className="bg-blue-600 hover:bg-blue-700 w-full sm:w-auto min-w-[180px] h-12 sm:h-14 text-base sm:text-lg">
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                    </svg>
                    Go Home
                  </Button>
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
