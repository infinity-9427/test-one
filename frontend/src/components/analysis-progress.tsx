'use client'

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

interface AnalysisProgressProps {
  progress: number;
}

const AnalysisProgress: React.FC<AnalysisProgressProps> = ({ 
  progress 
}) => {
  const stages = [
    { 
      name: 'Screenshot Capture', 
      duration: '10-15s',
      range: [0, 25],
      icon: '📸',
      description: 'Taking high-quality screenshots'
    },
    { 
      name: 'AI Vision Analysis', 
      duration: '20-30s',
      range: [25, 65],
      icon: '🤖',
      description: 'Analyzing design with AI vision models'
    },
    { 
      name: 'Rule-Based Scoring', 
      duration: '5-10s',
      range: [65, 85],
      icon: '📊',
      description: 'Calculating scores and metrics'
    },
    { 
      name: 'Report Generation', 
      duration: '5s',
      range: [85, 100],
      icon: '📄',
      description: 'Generating comprehensive report'
    }
  ];

  const getCurrentStageIndex = () => {
    return stages.findIndex(stage => 
      progress >= stage.range[0] && progress < stage.range[1]
    );
  };

  const currentStageIndex = getCurrentStageIndex();
  const activeStage = currentStageIndex >= 0 ? stages[currentStageIndex] : stages[stages.length - 1];

  const getEstimatedTimeRemaining = () => {
    if (progress >= 95) return 'Almost done...';
    
    const remainingProgress = 100 - progress;
    const estimatedSeconds = Math.ceil((remainingProgress / 100) * 60); // Rough estimate
    
    if (estimatedSeconds < 10) return 'Less than 10 seconds';
    if (estimatedSeconds < 30) return `About ${Math.ceil(estimatedSeconds / 5) * 5} seconds`;
    return `About ${Math.ceil(estimatedSeconds / 10) * 10} seconds`;
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader className="text-center">
        <CardTitle className="flex items-center justify-center gap-2 text-2xl">
          <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          Analyzing Website
        </CardTitle>
        <CardDescription className="text-lg">
          {getEstimatedTimeRemaining()} remaining
        </CardDescription>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Overall Progress Bar */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm text-gray-600">
            <span>Overall Progress</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-500 ease-out"
              style={{ width: `${Math.min(progress, 100)}%` }}
            />
          </div>
        </div>

        {/* Current Stage Highlight */}
        {currentStageIndex >= 0 && (
          <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-2xl">{activeStage.icon}</span>
              <div>
                <h3 className="font-semibold text-blue-900 dark:text-blue-100">
                  {activeStage.name}
                </h3>
                <p className="text-sm text-blue-700 dark:text-blue-300">
                  {activeStage.description}
                </p>
              </div>
            </div>
            <div className="text-xs text-blue-600 dark:text-blue-400">
              Estimated time: {activeStage.duration}
            </div>
          </div>
        )}

        {/* Stages Timeline */}
        <div className="space-y-3">
          <h4 className="font-medium text-gray-900 dark:text-gray-100">Analysis Stages</h4>
          <div className="space-y-2">
            {stages.map((stage, index) => {
              const isCompleted = progress > stage.range[1];
              const isActive = currentStageIndex === index;
              
              return (
                <div
                  key={stage.name}
                  className={`flex items-center gap-3 p-3 rounded-lg transition-all ${
                    isCompleted 
                      ? 'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800' 
                      : isActive 
                      ? 'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800' 
                      : 'bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700'
                  }`}
                >
                  <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                    isCompleted 
                      ? 'bg-green-500 text-white' 
                      : isActive 
                      ? 'bg-blue-500 text-white' 
                      : 'bg-gray-300 dark:bg-gray-600 text-gray-600 dark:text-gray-300'
                  }`}>
                    {isCompleted ? '✓' : index + 1}
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <h5 className={`font-medium ${
                        isCompleted 
                          ? 'text-green-900 dark:text-green-100' 
                          : isActive 
                          ? 'text-blue-900 dark:text-blue-100' 
                          : 'text-gray-600 dark:text-gray-300'
                      }`}>
                        {stage.icon} {stage.name}
                      </h5>
                      <span className={`text-xs ${
                        isCompleted 
                          ? 'text-green-600 dark:text-green-400' 
                          : isActive 
                          ? 'text-blue-600 dark:text-blue-400' 
                          : 'text-gray-500 dark:text-gray-400'
                      }`}>
                        {stage.duration}
                      </span>
                    </div>
                    <p className={`text-sm ${
                      isCompleted 
                        ? 'text-green-700 dark:text-green-300' 
                        : isActive 
                        ? 'text-blue-700 dark:text-blue-300' 
                        : 'text-gray-500 dark:text-gray-400'
                    }`}>
                      {stage.description}
                    </p>
                  </div>
                  
                  {isActive && (
                    <div className="flex-shrink-0">
                      <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Technical Note */}
        <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
          <p className="text-xs text-gray-600 dark:text-gray-400 text-center">
            <span className="font-medium">Note:</span> Analysis time may vary depending on website complexity, 
            image content, and current system load.
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default AnalysisProgress;
