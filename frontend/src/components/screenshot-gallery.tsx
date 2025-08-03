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
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            📸 Website Screenshots
            {websiteUrl && (
              <a 
                href={websiteUrl} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
              >
                Visit Site ↗
              </a>
            )}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            {/* Desktop Screenshot */}
            {desktopScreenshot && (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-gray-700 dark:text-gray-300">
                    🖥️ Desktop View
                  </h3>
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    {desktopScreenshot.width}×{desktopScreenshot.height}
                  </span>
                </div>
                
                <div className="relative group cursor-pointer" onClick={() => openFullSize(desktopScreenshot)}>
                  <div className="aspect-[4/3] relative overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800">
                    {imageLoading.desktop && (
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="w-8 h-8 border-2 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
                      </div>
                    )}
                    <Image
                      src={getImageUrl(desktopScreenshot, 'desktop')}
                      alt={`Desktop screenshot of ${websiteUrl || 'website'}`}
                      fill
                      className="object-cover transition-transform group-hover:scale-105"
                      onLoadStart={() => handleImageStart('desktop')}
                      onLoad={() => handleImageLoad('desktop')}
                      onError={() => handleImageError('desktop')}
                    />
                    
                    {/* Hover overlay */}
                    <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
                      <Button variant="secondary" size="sm">
                        🔍 Open Full Size
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Mobile Screenshot */}
            {mobileScreenshot && (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-gray-700 dark:text-gray-300">
                    📱 Mobile View
                  </h3>
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    {mobileScreenshot.width}×{mobileScreenshot.height}
                  </span>
                </div>
                
                <div className="flex justify-center">
                  <div className="relative group cursor-pointer max-w-[250px]" onClick={() => openFullSize(mobileScreenshot)}>
                    <div className="aspect-[9/16] relative overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800">
                      {imageLoading.mobile && (
                        <div className="absolute inset-0 flex items-center justify-center">
                          <div className="w-6 h-6 border-2 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
                        </div>
                      )}
                      <Image
                        src={getImageUrl(mobileScreenshot, 'mobile')}
                        alt={`Mobile screenshot of ${websiteUrl || 'website'}`}
                        fill
                        className="object-cover transition-transform group-hover:scale-105"
                        onLoadStart={() => handleImageStart('mobile')}
                        onLoad={() => handleImageLoad('mobile')}
                        onError={() => handleImageError('mobile')}
                      />
                      
                      {/* Hover overlay */}
                      <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
                        <Button variant="secondary" size="sm">
                          🔍 Open Full Size
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Screenshot info */}
          <div className="mt-4 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <p className="text-xs text-gray-600 dark:text-gray-400 text-center">
              💡 Click on any screenshot to open the full-size image in a new tab. Screenshots are optimized and stored securely.
            </p>
          </div>
        </CardContent>
      </Card>
    </>
  );
};

export default ScreenshotGallery;
