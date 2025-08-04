'use client'

import React, { useState } from 'react';
import Image from 'next/image';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface Screenshot {
  device: 'desktop' | 'mobile';
  url: string;
  cloudinary_url: string;
  width: number;
  height: number;
}

interface ScreenshotGalleryProps {
  screenshots: Screenshot[];
  loading?: boolean;
  websiteUrl?: string;
}

const ScreenshotGallery: React.FC<ScreenshotGalleryProps> = ({ 
  screenshots, 
  loading = false,
  websiteUrl 
}) => {
  const [imageLoading, setImageLoading] = useState<Record<string, boolean>>({});
  const [imageError, setImageError] = useState<Record<string, boolean>>({});

  const desktopScreenshot = screenshots.find(s => s.device === 'desktop');
  const mobileScreenshot = screenshots.find(s => s.device === 'mobile');

  const buildOptimizedUrl = (cloudinaryUrl: string, device: 'desktop' | 'mobile') => {
    // Return original URL if it doesn't look like a Cloudinary URL or if transformation fails
    if (!cloudinaryUrl.includes('cloudinary.com') || !cloudinaryUrl.includes('/upload/')) {
      return cloudinaryUrl;
    }

    try {
      // Extract the public_id from cloudinary URL
      const publicIdMatch = cloudinaryUrl.match(/\/upload\/(?:v\d+\/)?(.+)$/);
      if (!publicIdMatch) return cloudinaryUrl;
      
      const publicId = publicIdMatch[1];
      const baseUrl = cloudinaryUrl.split('/upload/')[0] + '/upload/';
      
      const transformations = device === 'desktop' 
        ? 'w_800,h_600,c_fit,q_auto,f_webp'
        : 'w_300,h_500,c_fit,q_auto,f_webp';
      
      return `${baseUrl}${transformations}/${publicId}`;
    } catch (error) {
      console.warn('Failed to build optimized URL, using original:', error);
      return cloudinaryUrl;
    }
  };

  const openFullSize = (screenshot: Screenshot) => {
    // Simple approach: just open the full-size image in a new tab
    window.open(screenshot.cloudinary_url || screenshot.url, '_blank');
  };

  const handleImageLoad = (device: string) => {
    setImageLoading(prev => ({ ...prev, [device]: false }));
    setImageError(prev => ({ ...prev, [device]: false }));
  };

  const handleImageStart = (device: string) => {
    setImageLoading(prev => ({ ...prev, [device]: true }));
    setImageError(prev => ({ ...prev, [device]: false }));
  };

  const handleImageError = (device: string) => {
    setImageLoading(prev => ({ ...prev, [device]: false }));
    setImageError(prev => ({ ...prev, [device]: true }));
  };

  const getImageUrl = (screenshot: Screenshot, device: 'desktop' | 'mobile') => {
    // If there was an error with the optimized URL, use the original
    if (imageError[device]) {
      return screenshot.cloudinary_url || screenshot.url;
    }
    // Otherwise try the optimized URL first
    return buildOptimizedUrl(screenshot.cloudinary_url, device);
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            📸 Website Screenshots
            <div className="w-4 h-4 border-2 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            {/* Desktop placeholder */}
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-700 dark:text-gray-300">Desktop View</h3>
              <div className="aspect-[4/3] bg-gray-200 dark:bg-gray-700 rounded-lg animate-pulse flex items-center justify-center">
                <div className="text-gray-400 dark:text-gray-500">Loading screenshot...</div>
              </div>
            </div>
            
            {/* Mobile placeholder */}
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-700 dark:text-gray-300">Mobile View</h3>
              <div className="aspect-[9/16] bg-gray-200 dark:bg-gray-700 rounded-lg animate-pulse flex items-center justify-center max-w-[200px] mx-auto">
                <div className="text-gray-400 dark:text-gray-500 text-sm text-center">Loading screenshot...</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!screenshots.length) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>📸 Website Screenshots</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-gray-500 dark:text-gray-400">
            No screenshots available
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <>
      <Card className="overflow-hidden">
        <CardHeader className="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20">
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              📸 Website Screenshots
              <span className="text-sm font-normal text-gray-600 dark:text-gray-400">
                ({screenshots.length} captured)
              </span>
            </div>
            {websiteUrl && (
              <a 
                href={websiteUrl} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-sm text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1 bg-white/80 dark:bg-gray-800/80 px-3 py-1 rounded-full border"
              >
                🌐 Visit Site ↗
              </a>
            )}
          </CardTitle>
        </CardHeader>
        <CardContent className="p-6">
          <div className="grid md:grid-cols-2 gap-8">
            {/* Desktop Screenshot */}
            {desktopScreenshot && (
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-800 rounded-lg border">
                  <h3 className="font-semibold text-gray-800 dark:text-gray-200 flex items-center gap-2">
                    🖥️ Desktop View
                    <span className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded">
                      Primary
                    </span>
                  </h3>
                  <span className="text-xs text-gray-500 dark:text-gray-400 font-mono bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
                    {desktopScreenshot.width}×{desktopScreenshot.height}
                  </span>
                </div>
                
                <div className="relative group cursor-pointer" onClick={() => openFullSize(desktopScreenshot)}>
                  <div className="aspect-[4/3] relative overflow-hidden rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800 shadow-lg">
                    {imageLoading.desktop && (
                      <div className="absolute inset-0 flex items-center justify-center bg-gray-50 dark:bg-gray-800">
                        <div className="flex flex-col items-center gap-3">
                          <div className="w-8 h-8 border-2 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
                          <span className="text-sm text-gray-600 dark:text-gray-400">Loading desktop view...</span>
                        </div>
                      </div>
                    )}
                    <Image
                      src={getImageUrl(desktopScreenshot, 'desktop')}
                      alt={`Desktop screenshot of ${websiteUrl || 'website'}`}
                      fill
                      className="object-cover transition-all duration-300 group-hover:scale-105"
                      onLoadStart={() => handleImageStart('desktop')}
                      onLoad={() => handleImageLoad('desktop')}
                      onError={() => handleImageError('desktop')}
                    />
                    
                    {/* Enhanced hover overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-black/20 opacity-0 group-hover:opacity-100 transition-all duration-300 flex items-center justify-center">
                      <div className="transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
                        <Button variant="secondary" size="sm" className="bg-white/90 hover:bg-white text-gray-800 font-semibold shadow-lg">
                          🔍 View Full Size
                        </Button>
                      </div>
                    </div>
                    
                    {/* Corner indicator */}
                    <div className="absolute top-3 right-3 bg-blue-500 text-white text-xs px-2 py-1 rounded-full opacity-90">
                      Desktop
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Mobile Screenshot */}
            {mobileScreenshot && (
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-800 rounded-lg border">
                  <h3 className="font-semibold text-gray-800 dark:text-gray-200 flex items-center gap-2">
                    📱 Mobile View
                    <span className="text-xs bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-2 py-1 rounded">
                      Responsive
                    </span>
                  </h3>
                  <span className="text-xs text-gray-500 dark:text-gray-400 font-mono bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
                    {mobileScreenshot.width}×{mobileScreenshot.height}
                  </span>
                </div>
                
                <div className="flex justify-center">
                  <div className="relative group cursor-pointer max-w-[280px]" onClick={() => openFullSize(mobileScreenshot)}>
                    <div className="aspect-[9/16] relative overflow-hidden rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800 shadow-lg">
                      {imageLoading.mobile && (
                        <div className="absolute inset-0 flex items-center justify-center bg-gray-50 dark:bg-gray-800">
                          <div className="flex flex-col items-center gap-3">
                            <div className="w-6 h-6 border-2 border-gray-300 border-t-green-500 rounded-full animate-spin"></div>
                            <span className="text-xs text-gray-600 dark:text-gray-400">Loading mobile view...</span>
                          </div>
                        </div>
                      )}
                      <Image
                        src={getImageUrl(mobileScreenshot, 'mobile')}
                        alt={`Mobile screenshot of ${websiteUrl || 'website'}`}
                        fill
                        className="object-cover transition-all duration-300 group-hover:scale-105"
                        onLoadStart={() => handleImageStart('mobile')}
                        onLoad={() => handleImageLoad('mobile')}
                        onError={() => handleImageError('mobile')}
                      />
                      
                      {/* Enhanced hover overlay */}
                      <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-black/20 opacity-0 group-hover:opacity-100 transition-all duration-300 flex items-center justify-center">
                        <div className="transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
                          <Button variant="secondary" size="sm" className="bg-white/90 hover:bg-white text-gray-800 font-semibold shadow-lg">
                            🔍 View Full Size
                          </Button>
                        </div>
                      </div>
                      
                      {/* Corner indicator */}
                      <div className="absolute top-3 right-3 bg-green-500 text-white text-xs px-2 py-1 rounded-full opacity-90">
                        Mobile
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Enhanced info section */}
          <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-xl border border-blue-200 dark:border-blue-800">
            <div className="flex items-start gap-3">
              <div className="text-2xl">💡</div>
              <div>
                <p className="text-sm font-medium text-gray-800 dark:text-gray-200 mb-1">
                  Interactive Screenshots
                </p>
                <p className="text-xs text-gray-600 dark:text-gray-400">
                  Click on any screenshot to view the full-resolution image. These captures show how your website appears to visitors on different devices.
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </>
  );
};

export default ScreenshotGallery;
