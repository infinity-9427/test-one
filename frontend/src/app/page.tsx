'use client'

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { PDFReport, ReportData } from '@/components/pdf-report';

export default function Home() {
  const [url, setUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [reportData, setReportData] = useState<ReportData | null>(null);
  const [error, setError] = useState('');

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
      setError('Please enter a URL');
      return;
    }

    if (!validateUrl(url)) {
      setError('Please enter a valid URL (include http:// or https://)');
      return;
    }

    setError('');
    setIsAnalyzing(true);

    try {
      // Simulate the analysis process with potential failure
      await new Promise((resolve, reject) => {
        setTimeout(() => {
          // Simulate occasional failures for demo purposes
          if (Math.random() < 0.1) { // 10% chance of failure
            reject(new Error('Failed to connect to the website'));
          } else {
            resolve(null);
          }
        }, 3000);
      });

      // Mock report data - in real implementation, this would come from your analysis engine
      const mockReportData: ReportData = {
        url: url,
        overallScore: 78,
        typography: {
          score: 85,
          issues: [
            'Small font size detected on mobile devices',
            'Insufficient line height in paragraph text'
          ],
          recommendations: [
            'Increase minimum font size to 16px for mobile',
            'Adjust line height to 1.5 for better readability'
          ]
        },
        color: {
          score: 72,
          issues: [
            'Low contrast ratio between text and background',
            'Missing focus indicators on interactive elements'
          ],
          recommendations: [
            'Increase contrast ratio to meet WCAG AA standards',
            'Add visible focus states for keyboard navigation'
          ]
        },
        layout: {
          score: 76,
          issues: [
            'Inconsistent spacing between sections',
            'No clear visual hierarchy'
          ],
          recommendations: [
            'Implement consistent spacing system',
            'Use typography scale to establish hierarchy'
          ]
        },
        timestamp: new Date()
      };

      setReportData(mockReportData);
    } catch (err) {
      if (err instanceof Error) {
        setError(`Analysis failed: ${err.message}. Please check the URL and try again.`);
      } else {
        setError('Failed to analyze the website. Please try again.');
      }
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUrl(e.target.value);
    if (error) setError('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
              Design Scoring & Reporting Tool
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Analyze any website's design with AI-powered assessment and get professional reports
            </p>
          </div>

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
                      placeholder="https://example.com"
                      value={url}
                      onChange={handleUrlChange}
                      className="h-12 text-base flex-1"
                      disabled={isAnalyzing}
                    />
                    <Button 
                      onClick={handleAnalyze}
                      disabled={isAnalyzing || !url.trim()}
                      className="h-12 px-8 bg-blue-600 hover:bg-blue-700"
                    >
                      {isAnalyzing ? (
                        <div className="flex items-center gap-2">
                          <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
                          Analyzing...
                        </div>
                      ) : (
                        'Analyze'
                      )}
                    </Button>
                  </div>
                  {error && (
                    <p className="text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 p-3 rounded-lg">
                      {error}
                    </p>
                  )}
                </div>

                {/* Features */}
                <div className="grid md:grid-cols-3 gap-4 pt-4">
                  <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <div className="text-2xl mb-2">📸</div>
                    <h3 className="font-semibold text-gray-900 dark:text-white">Screenshot</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300">High-quality capture</p>
                  </div>
                  <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                    <div className="text-2xl mb-2">🎨</div>
                    <h3 className="font-semibold text-gray-900 dark:text-white">AI Analysis</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300">Design evaluation</p>
                  </div>
                  <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                    <div className="text-2xl mb-2">📊</div>
                    <h3 className="font-semibold text-gray-900 dark:text-white">Reports</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300">Professional PDF</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Results Section */}
          {reportData && (
            <Card className="shadow-lg">
              <CardHeader className="text-center">
                <CardTitle className="text-3xl text-green-600 dark:text-green-400 flex items-center justify-center gap-2">
                  <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  Analysis Complete
                </CardTitle>
                <CardDescription className="text-lg">
                  Your design analysis is ready
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-8">
                {/* Overall Score */}
                <div className="text-center p-6 bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 rounded-xl">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Overall Score</h3>
                  <div className="text-5xl font-bold text-green-600 dark:text-green-400">
                    {reportData.overallScore}/100
                  </div>
                </div>

                {/* Score Breakdown */}
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="text-center p-6 bg-blue-50 dark:bg-blue-900/20 rounded-xl">
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Typography</h4>
                    <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">
                      {reportData.typography.score}
                    </p>
                  </div>
                  <div className="text-center p-6 bg-purple-50 dark:bg-purple-900/20 rounded-xl">
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Color & Accessibility</h4>
                    <p className="text-3xl font-bold text-purple-600 dark:text-purple-400">
                      {reportData.color.score}
                    </p>
                  </div>
                  <div className="text-center p-6 bg-orange-50 dark:bg-orange-900/20 rounded-xl">
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Layout & Structure</h4>
                    <p className="text-3xl font-bold text-orange-600 dark:text-orange-400">
                      {reportData.layout.score}
                    </p>
                  </div>
                </div>

                {/* Download Report */}
                <div className="text-center pt-4 border-t">
                  <PDFReport data={reportData} />
                  <p className="text-sm text-gray-600 dark:text-gray-300 mt-2">
                    Download detailed PDF report with recommendations
                  </p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
