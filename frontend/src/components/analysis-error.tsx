'use client'

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface AnalysisErrorProps {
  error: string;
  onRetry?: () => void;
  onReset?: () => void;
}

interface ErrorInfo {
  type: 'network' | 'analysis' | 'validation' | 'timeout' | 'server' | 'unknown';
  title: string;
  description: string;
  retryable: boolean;
  suggestedAction: string;
  icon: string;
}

const parseAnalysisError = (error: string): ErrorInfo => {
  const errorLower = error.toLowerCase();

  // Network/Connection errors
  if (errorLower.includes('unable to connect') || errorLower.includes('network') || errorLower.includes('fetch')) {
    return {
      type: 'network',
      title: 'Connection Error',
      description: 'Unable to connect to the analysis service.',
      retryable: true,
      suggestedAction: 'Check your internet connection and try again.',
      icon: '🌐'
    };
  }

  // Timeout errors
  if (errorLower.includes('timeout') || errorLower.includes('timed out')) {
    return {
      type: 'timeout',
      title: 'Request Timeout',
      description: 'The analysis took too long to complete.',
      retryable: true,
      suggestedAction: 'The website may be slow to load. Please try again or try a different URL.',
      icon: '⏰'
    };
  }

  // Server errors
  if (errorLower.includes('service unavailable') || errorLower.includes('temporarily unavailable')) {
    return {
      type: 'server',
      title: 'Service Unavailable',
      description: 'The analysis service is temporarily unavailable.',
      retryable: true,
      suggestedAction: 'Please wait a moment and try again.',
      icon: '🔧'
    };
  }

  // Validation errors
  if (errorLower.includes('invalid url') || errorLower.includes('not found') || errorLower.includes('inaccessible')) {
    return {
      type: 'validation',
      title: 'Invalid URL',
      description: 'The provided URL is invalid or the website is not accessible.',
      retryable: false,
      suggestedAction: 'Please check the URL and ensure it includes http:// or https://.',
      icon: '🔗'
    };
  }

  // Rate limiting
  if (errorLower.includes('too many requests') || errorLower.includes('rate limit')) {
    return {
      type: 'server',
      title: 'Rate Limited',
      description: 'Too many requests have been made.',
      retryable: true,
      suggestedAction: 'Please wait a few minutes before trying again.',
      icon: '🚦'
    };
  }

  // Analysis specific errors
  if (errorLower.includes('analysis failed') || errorLower.includes('screenshot failed')) {
    return {
      type: 'analysis',
      title: 'Analysis Failed',
      description: 'The website analysis could not be completed.',
      retryable: true,
      suggestedAction: 'This might be due to website restrictions or complex content. Try again or contact support.',
      icon: '📊'
    };
  }

  // Generic/Unknown errors
  return {
    type: 'unknown',
    title: 'Unexpected Error',
    description: 'An unexpected error occurred during analysis.',
    retryable: true,
    suggestedAction: 'Please try again. If the problem persists, contact support.',
    icon: '⚠️'
  };
};

const AnalysisError: React.FC<AnalysisErrorProps> = ({ error, onRetry, onReset }) => {
  const errorInfo = parseAnalysisError(error);

  const getErrorColors = (type: string) => {
    switch (type) {
      case 'network':
        return 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800 text-blue-900 dark:text-blue-100';
      case 'timeout':
        return 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800 text-yellow-900 dark:text-yellow-100';
      case 'validation':
        return 'bg-orange-50 dark:bg-orange-900/20 border-orange-200 dark:border-orange-800 text-orange-900 dark:text-orange-100';
      case 'server':
        return 'bg-purple-50 dark:bg-purple-900/20 border-purple-200 dark:border-purple-800 text-purple-900 dark:text-purple-100';
      case 'analysis':
        return 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800 text-red-900 dark:text-red-100';
      default:
        return 'bg-gray-50 dark:bg-gray-900/20 border-gray-200 dark:border-gray-800 text-gray-900 dark:text-gray-100';
    }
  };

  return (
    <Card className={`border-2 ${getErrorColors(errorInfo.type)}`}>
      <CardHeader className="text-center">
        <CardTitle className="flex items-center justify-center gap-3 text-2xl">
          <span className="text-4xl">{errorInfo.icon}</span>
          {errorInfo.title}
        </CardTitle>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Error Description */}
        <div className="text-center space-y-2">
          <p className="text-lg font-medium">
            {errorInfo.description}
          </p>
          <p className="text-sm opacity-80">
            {errorInfo.suggestedAction}
          </p>
        </div>

        {/* Original Error Message */}
        <details className="p-3 bg-white dark:bg-gray-900 bg-opacity-50 rounded-lg border">
          <summary className="cursor-pointer text-sm font-medium opacity-75 hover:opacity-100">
            Technical Details
          </summary>
          <div className="mt-2 p-2 bg-gray-100 dark:bg-gray-800 rounded text-xs font-mono text-gray-700 dark:text-gray-300 break-all">
            {error}
          </div>
        </details>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          {errorInfo.retryable && onRetry && (
            <Button 
              onClick={onRetry} 
              variant="default"
              className="flex items-center gap-2"
            >
              🔄 Try Again
            </Button>
          )}
          
          {onReset && (
            <Button 
              onClick={onReset} 
              variant="outline"
              className="flex items-center gap-2"
            >
              🏠 Start Over
            </Button>
          )}
          
          <Button 
            variant="ghost"
            onClick={() => window.location.reload()}
            className="flex items-center gap-2"
          >
            ↻ Refresh Page
          </Button>
        </div>

        {/* Troubleshooting Tips */}
        <div className="p-4 bg-white dark:bg-gray-900 bg-opacity-30 rounded-lg">
          <h4 className="font-medium mb-2 flex items-center gap-2">
            💡 Troubleshooting Tips
          </h4>
          <ul className="text-sm space-y-1 opacity-90">
            {errorInfo.type === 'validation' && (
              <>
                <li>• Make sure the URL starts with http:// or https://</li>
                <li>• Verify the website is publicly accessible</li>
                <li>• Try a different URL to test the service</li>
              </>
            )}
            {errorInfo.type === 'network' && (
              <>
                <li>• Check your internet connection</li>
                <li>• Try refreshing the page</li>
                <li>• Contact support if the issue persists</li>
              </>
            )}
            {errorInfo.type === 'timeout' && (
              <>
                <li>• The website might be slow to load</li>
                <li>• Try a simpler or faster website</li>
                <li>• Wait a moment and try again</li>
              </>
            )}
            {errorInfo.type === 'server' && (
              <>
                <li>• The service might be under maintenance</li>
                <li>• Wait a few minutes and try again</li>
                <li>• Check our status page for updates</li>
              </>
            )}
            {(errorInfo.type === 'analysis' || errorInfo.type === 'unknown') && (
              <>
                <li>• The website might have restrictions</li>
                <li>• Try a different website</li>
                <li>• Contact support if the problem continues</li>
              </>
            )}
          </ul>
        </div>

        {/* Support Contact */}
        <div className="text-center">
          <p className="text-sm opacity-75">
            Need help? Contact our support team for assistance.
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default AnalysisError;
