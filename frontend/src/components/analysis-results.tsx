'use client'

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AnalysisResponse } from '@/lib/api-client';
import ScoreDisplay from '@/components/score-display';
import ScreenshotGallery from '@/components/screenshot-gallery';
import { PDFReport } from '@/components/pdf-report';

interface AnalysisResultsProps {
  analysis: AnalysisResponse;
  onStartNew?: () => void;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ analysis, onStartNew }) => {
  const formatDuration = (seconds: number): string => {
    if (seconds < 60) {
      return `${seconds.toFixed(1)} seconds`;
    }
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds.toFixed(1)}s`;
  };

  const getScoreGrade = (score: number): string => {
    if (score >= 90) return 'A';
    if (score >= 80) return 'B';
    if (score >= 70) return 'C';
    if (score >= 60) return 'D';
    return 'F';
  };

  const getStatusBadge = (status: string) => {
    const badgeColors = {
      completed: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
      processing: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
      failed: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
    };

    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${badgeColors[status as keyof typeof badgeColors] || badgeColors.completed}`}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  return (
    <div className="space-y-8">
      {/* Header Section */}
      <Card className="border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl text-green-600 dark:text-green-400 flex items-center justify-center gap-3">
            <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            Analysis Complete
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center space-y-4">
            {/* Website Info */}
            <div className="p-4 bg-white dark:bg-gray-800 rounded-lg border">
              <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">Website Analyzed</h3>
              <a 
                href={analysis.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-600 dark:text-blue-400 hover:underline text-lg font-medium break-all"
              >
                {analysis.url}
              </a>
              <div className="flex items-center justify-center gap-4 mt-3 text-sm text-gray-600 dark:text-gray-400">
                <span>ID: {analysis.analysis_id}</span>
                <span>•</span>
                {getStatusBadge(analysis.status)}
                <span>•</span>
                <span>Duration: {formatDuration(analysis.analysis_duration)}</span>
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                Completed on {new Date(analysis.completed_at).toLocaleDateString()} at {new Date(analysis.completed_at).toLocaleTimeString()}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <PDFReport data={analysis} />
              {onStartNew && (
                <Button variant="outline" onClick={onStartNew} className="flex items-center gap-2">
                  🔄 Analyze Another Website
                </Button>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Overall Score Card */}
      <Card className="text-center">
        <CardContent className="pt-8">
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
              Overall Design Score
            </h3>
            
            <div className="flex items-center justify-center gap-6">
              <div className="text-center">
                <div className="text-6xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                  {analysis.overall_score}
                </div>
                <div className="text-gray-600 dark:text-gray-400 text-lg">out of 100</div>
              </div>
              
              <div className="text-center">
                <div className={`w-20 h-20 rounded-full flex items-center justify-center text-3xl font-bold text-white mb-2 ${
                  analysis.overall_score >= 90 ? 'bg-green-500' :
                  analysis.overall_score >= 80 ? 'bg-blue-500' :
                  analysis.overall_score >= 70 ? 'bg-yellow-500' :
                  analysis.overall_score >= 60 ? 'bg-orange-500' : 'bg-red-500'
                }`}>
                  {getScoreGrade(analysis.overall_score)}
                </div>
                <div className="text-gray-600 dark:text-gray-400">Grade</div>
              </div>
            </div>

            <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              {analysis.overall_score >= 90 ? 
                'Excellent! This website demonstrates outstanding design principles with minimal areas for improvement.' :
                analysis.overall_score >= 80 ? 
                'Great design with strong fundamentals. A few enhancements could elevate it further.' :
                analysis.overall_score >= 70 ? 
                'Good foundation with several opportunities for improvement to enhance user experience.' :
                analysis.overall_score >= 60 ? 
                'The design has potential but needs attention in multiple areas to meet modern standards.' :
                'Significant improvements needed across design fundamentals to create an effective user experience.'
              }
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Screenshots */}
      <ScreenshotGallery 
        screenshots={analysis.screenshots} 
        websiteUrl={analysis.url}
      />

      {/* Detailed Scores */}
      <ScoreDisplay 
        scores={analysis.scores_breakdown} 
        overallScore={analysis.overall_score} 
      />



      {/* Technical Details */}
      {Object.keys(analysis.errors).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-orange-600 dark:text-orange-400">
              ⚠️ Analysis Warnings
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {Object.entries(analysis.errors).map(([category, error]) => (
                <div key={category} className="p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-800">
                  <div className="font-medium text-orange-900 dark:text-orange-100 capitalize">
                    {category.replace('_', ' ')}
                  </div>
                  <div className="text-sm text-orange-700 dark:text-orange-300">
                    {error}
                  </div>
                </div>
              ))}
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-4">
              These warnings indicate parts of the analysis that encountered issues but didn&apos;t prevent completion.
            </p>
          </CardContent>
        </Card>
      )}

      {/* Simple Analysis Info */}
      <Card>
        <CardContent className="pt-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div className="text-center">
              <div className="font-medium text-gray-900 dark:text-gray-100">Status</div>
              <div className="text-gray-600 dark:text-gray-400">{analysis.status}</div>
            </div>
            
            <div className="text-center">
              <div className="font-medium text-gray-900 dark:text-gray-100">Duration</div>
              <div className="text-gray-600 dark:text-gray-400">{formatDuration(analysis.analysis_duration)}</div>
            </div>
            
            <div className="text-center">
              <div className="font-medium text-gray-900 dark:text-gray-100">AI Model</div>
              <div className="text-gray-600 dark:text-gray-400">{analysis.ai_insights.llm_analysis.model_used}</div>
            </div>
            
            <div className="text-center">
              <div className="font-medium text-gray-900 dark:text-gray-100">Screenshots</div>
              <div className="text-gray-600 dark:text-gray-400">{analysis.screenshots.length} captured</div>
            </div>
          </div>
        </CardContent>
      </Card>


    </div>
  );
};

export default AnalysisResults;
