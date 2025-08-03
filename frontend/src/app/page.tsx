'use client'

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useAnalysis } from '@/hooks/useAnalysis';
import AnalysisProgress from '@/components/analysis-progress';
import AnalysisResults from '@/components/analysis-results';
import AnalysisError from '@/components/analysis-error';

export default function Home() {
  const [url, setUrl] = useState('');
  const {
    isAnalyzing,
    analysisProgress,
    currentAnalysis,
    error,
    backendHealth,
    analyzeWebsite,
    clearError,
    resetAnalysis,
    checkBackendHealth
  } = useAnalysis();

  // Check backend health on component mount
  useEffect(() => {
    checkBackendHealth();
  }, [checkBackendHealth]);

  const validateUrl = (inputUrl: string): boolean => {
    try {
      new URL(inputUrl);
      return true;
    } catch {
      return false;
    }
  };

  const handleAnalyze = async () => {
    if (!url.trim()) {
      return;
    }

    let processedUrl = url.trim();
    
    // Add protocol if missing
    if (!processedUrl.match(/^https?:\/\//)) {
      processedUrl = 'https://' + processedUrl;
    }

    if (!validateUrl(processedUrl)) {
      return;
    }

    await analyzeWebsite(processedUrl, {
      autoLogToSheets: true,
      includeMobile: true
    });
  };

  const handleUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUrl(e.target.value);
    if (error) clearError();
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && url.trim() && !isAnalyzing) {
      handleAnalyze();
    }
  };

  const handleStartNew = () => {
    resetAnalysis();
    setUrl('');
  };

  // Show results if we have a completed analysis
  if (currentAnalysis && !isAnalyzing) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-6xl mx-auto">
            <AnalysisResults 
              analysis={currentAnalysis} 
              onStartNew={handleStartNew}
            />
          </div>
        </div>
      </div>
    );
  }

  // Show error state
  if (error && !isAnalyzing) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="text-center mb-8">
              <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
                Design Scoring & Reporting Tool
              </h1>
              <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
                AI-powered website design analysis with professional insights
              </p>
            </div>

            <AnalysisError 
              error={error} 
              onRetry={() => {
                clearError();
                if (url.trim()) {
                  handleAnalyze();
                }
              }}
              onReset={handleStartNew}
            />
          </div>
        </div>
      </div>
    );
  }

  // Show analysis progress
  if (isAnalyzing) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="text-center mb-8">
              <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
                Design Scoring & Reporting Tool
              </h1>
              <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
                Analyzing <span className="font-semibold text-blue-600 dark:text-blue-400">{url}</span>
              </p>
            </div>

            <AnalysisProgress progress={analysisProgress} />
          </div>
        </div>
      </div>
    );
  }

  // Show main input form (default state)
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
              AI-Powered Design Analysis
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Get professional insights on your website&apos;s design with comprehensive AI analysis and actionable recommendations
            </p>
          </div>

          {/* Backend Health Status */}
          {backendHealth.status !== 'unknown' && (
            <div className="mb-6">
              <div className={`p-3 rounded-lg text-center text-sm ${
                backendHealth.status === 'healthy' 
                  ? 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-800'
                  : 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800'
              }`}>
                <span className="font-medium">
                  {backendHealth.status === 'healthy' ? '✅ Service Online' : '❌ Service Unavailable'}
                </span>
                {backendHealth.lastChecked && (
                  <span className="ml-2 opacity-75">
                    • Last checked: {backendHealth.lastChecked.toLocaleTimeString()}
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Main Analysis Card */}
          <Card className="mb-8 shadow-lg">
            <CardContent className="p-8">
              <div className="space-y-6">
                <div className="space-y-4">
                  <label htmlFor="url-input" className="text-lg font-semibold text-gray-900 dark:text-white">
                    Website URL
                  </label>
                  <div className="flex gap-4">
                    <Input
                      id="url-input"
                      type="url"
                      placeholder="https://example.com or example.com"
                      value={url}
                      onChange={handleUrlChange}
                      onKeyPress={handleKeyPress}
                      className="h-12 text-base flex-1"
                      disabled={isAnalyzing}
                    />
                    <Button 
                      onClick={handleAnalyze}
                      disabled={isAnalyzing || !url.trim() || backendHealth.status === 'unhealthy'}
                      className="h-12 px-8 bg-blue-600 hover:bg-blue-700"
                    >
                      Analyze Website
                    </Button>
                  </div>
                  
                  {backendHealth.status === 'unhealthy' && (
                    <p className="text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 p-3 rounded-lg">
                      ⚠️ Analysis service is currently unavailable. Please try again later.
                    </p>
                  )}
                </div>

                {/* Features */}
                <div className="grid md:grid-cols-3 gap-4 pt-4">
                  <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <div className="text-2xl mb-2">📸</div>
                    <h3 className="font-semibold text-gray-900 dark:text-white">Screenshot Capture</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300">High-quality desktop & mobile screenshots</p>
                  </div>
                  <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                    <div className="text-2xl mb-2">🤖</div>
                    <h3 className="font-semibold text-gray-900 dark:text-white">AI Vision Analysis</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300">Advanced ML models analyze design</p>
                  </div>
                  <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                    <div className="text-2xl mb-2">📊</div>
                    <h3 className="font-semibold text-gray-900 dark:text-white">Professional Reports</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300">Downloadable PDF with insights</p>
                  </div>
                </div>

                {/* Analysis Categories */}
                <div className="mt-8">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 text-center">
                    What We Analyze
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                    {[
                      { icon: '🎨', label: 'Design Principles' },
                      { icon: '♿', label: 'Accessibility' },
                      { icon: '📐', label: 'Visual Hierarchy' },
                      { icon: '🌈', label: 'Color Theory' },
                      { icon: '📝', label: 'Typography' },
                      { icon: '📋', label: 'Layout & Composition' },
                      { icon: '👥', label: 'User Experience' },
                      { icon: '📱', label: 'Mobile Responsiveness' }
                    ].map((item, index) => (
                      <div key={index} className="flex items-center gap-2 p-2 bg-gray-50 dark:bg-gray-800 rounded text-gray-700 dark:text-gray-300">
                        <span>{item.icon}</span>
                        <span className="text-xs">{item.label}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* How it Works */}
          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle className="text-center">How It Works</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-4 gap-6">
                <div className="text-center">
                  <div className="w-12 h-12 bg-blue-500 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">1</div>
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Enter URL</h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Provide the website URL you want to analyze</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-green-500 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">2</div>
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-2">AI Analysis</h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Our AI captures screenshots and analyzes design elements</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-purple-500 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">3</div>
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Generate Insights</h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Receive detailed scores and actionable recommendations</p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-orange-500 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">4</div>
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Download Report</h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Get a professional PDF report with all findings</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
