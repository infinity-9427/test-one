'use client'

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface ScoresBreakdown {
  design_principles: number;
  accessibility: number;
  visual_hierarchy: number;
  color_theory: number;
  typography: number;
  layout_composition: number;
  user_experience: number;
  mobile_responsiveness: number;
}

interface ScoreDisplayProps {
  scores: ScoresBreakdown;
  overallScore: number;
  loading?: boolean;
}

interface AnimatedCounterProps {
  value: number;
  duration?: number;
  suffix?: string;
}

const AnimatedCounter: React.FC<AnimatedCounterProps> = ({ 
  value, 
  duration = 2000, 
  suffix = '' 
}) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTime: number;
    let animationFrame: number;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = (timestamp - startTime) / duration;

      if (progress < 1) {
        // Easing function for smooth animation
        const easeOutCubic = 1 - Math.pow(1 - progress, 3);
        setCount(Math.floor(easeOutCubic * value));
        animationFrame = requestAnimationFrame(animate);
      } else {
        setCount(value);
      }
    };

    animationFrame = requestAnimationFrame(animate);

    return () => {
      if (animationFrame) {
        cancelAnimationFrame(animationFrame);
      }
    };
  }, [value, duration]);

  return <span>{count}{suffix}</span>;
};

const getScoreColor = (score: number): string => {
  if (score >= 90) return 'text-green-600 dark:text-green-400';
  if (score >= 80) return 'text-lime-600 dark:text-lime-400';
  if (score >= 70) return 'text-yellow-600 dark:text-yellow-400';
  if (score >= 60) return 'text-orange-600 dark:text-orange-400';
  return 'text-red-600 dark:text-red-400';
};

const getScoreGrade = (score: number): string => {
  if (score >= 90) return 'A';
  if (score >= 80) return 'B';
  if (score >= 70) return 'C';
  if (score >= 60) return 'D';
  return 'F';
};

const getScoreBgColor = (score: number): string => {
  if (score >= 90) return 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800';
  if (score >= 80) return 'bg-lime-50 dark:bg-lime-900/20 border-lime-200 dark:border-lime-800';
  if (score >= 70) return 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800';
  if (score >= 60) return 'bg-orange-50 dark:bg-orange-900/20 border-orange-200 dark:border-orange-800';
  return 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800';
};

interface ScoreCardProps {
  category: string;
  score: number;
  icon: string;
  description: string;
}

const ScoreCard: React.FC<ScoreCardProps> = ({ category, score, icon, description }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  return (
    <div 
      className={`p-4 rounded-lg border ${getScoreBgColor(score)} transition-all hover:shadow-md cursor-pointer`}
      onClick={() => setIsExpanded(!isExpanded)}
    >
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className="text-xl">{icon}</span>
          <h4 className="font-semibold text-gray-900 dark:text-gray-100 text-sm">{category}</h4>
        </div>
        <div className={`text-lg font-bold ${getScoreColor(score)} flex items-center gap-1`}>
          <AnimatedCounter value={score} />
          <span className="text-xs font-normal opacity-75">/{100}</span>
        </div>
      </div>
      
      <div className="flex items-center justify-between">
        <p className="text-xs text-gray-600 dark:text-gray-400 flex-1">{description}</p>
        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white ml-2 ${
          score >= 90 ? 'bg-green-500' :
          score >= 80 ? 'bg-lime-500' :
          score >= 70 ? 'bg-yellow-500' :
          score >= 60 ? 'bg-orange-500' : 'bg-red-500'
        }`}>
          {getScoreGrade(score)}
        </div>
      </div>
      
      {/* Progress bar */}
      <div className="mt-3 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
        <div 
          className={`h-2 rounded-full transition-all duration-1000 ease-out ${
            score >= 90 ? 'bg-green-500' :
            score >= 80 ? 'bg-lime-500' :
            score >= 70 ? 'bg-yellow-500' :
            score >= 60 ? 'bg-orange-500' : 'bg-red-500'
          }`}
          style={{ width: `${score}%` }}
        />
      </div>

      {/* Score interpretation */}
      <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
        {score >= 90 ? 'Excellent performance' :
         score >= 80 ? 'Good with minor improvements' :
         score >= 70 ? 'Average with room for improvement' :
         score >= 60 ? 'Below average, needs attention' :
         'Poor, requires significant work'}
      </div>


    </div>
  );
};

const ScoreDisplay: React.FC<ScoreDisplayProps> = ({ scores, overallScore, loading = false }) => {
  const categoryConfig = {
    design_principles: { 
      icon: '🎨', 
      label: 'Design Principles',
      description: 'Visual balance, contrast, emphasis'
    },
    accessibility: { 
      icon: '♿', 
      label: 'Accessibility',
      description: 'WCAG compliance, inclusivity'
    },
    visual_hierarchy: { 
      icon: '📐', 
      label: 'Visual Hierarchy',
      description: 'Information organization, flow'
    },
    color_theory: { 
      icon: '🌈', 
      label: 'Color Theory',
      description: 'Color harmony, psychology'
    },
    typography: { 
      icon: '📝', 
      label: 'Typography',
      description: 'Font choices, readability'
    },
    layout_composition: { 
      icon: '📋', 
      label: 'Layout & Composition',
      description: 'Grid system, spacing, alignment'
    },
    user_experience: { 
      icon: '👥', 
      label: 'User Experience',
      description: 'Usability, navigation, flow'
    },
    mobile_responsiveness: { 
      icon: '📱', 
      label: 'Mobile Responsiveness',
      description: 'Mobile optimization, adaptive design'
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            📊 Design Scores
            <div className="w-4 h-4 border-2 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {/* Overall score placeholder */}
            <div className="text-center p-6 bg-gray-100 dark:bg-gray-800 rounded-xl animate-pulse">
              <div className="h-8 bg-gray-300 dark:bg-gray-600 rounded mb-2 w-48 mx-auto"></div>
              <div className="h-16 bg-gray-300 dark:bg-gray-600 rounded w-32 mx-auto"></div>
            </div>
            
            {/* Category scores placeholder */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Array.from({ length: 8 }).map((_, index) => (
                <div key={index} className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg animate-pulse">
                  <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded mb-2"></div>
                  <div className="h-6 bg-gray-300 dark:bg-gray-600 rounded w-16"></div>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>📊 Design Scores</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Overall Score */}
        <div className={`text-center p-8 rounded-xl border ${getScoreBgColor(overallScore)} relative overflow-hidden`}>
          {/* Background decoration */}
          <div className="absolute inset-0 opacity-5">
            <div className="absolute top-4 right-4 text-6xl">📊</div>
            <div className="absolute bottom-4 left-4 text-4xl">✨</div>
          </div>
          
          <div className="relative z-10">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              🏆 Overall Design Score
            </h3>
            <div className="flex items-center justify-center gap-6 mb-4">
              <div className={`text-7xl font-bold ${getScoreColor(overallScore)} drop-shadow-lg`}>
                <AnimatedCounter value={overallScore} suffix="/100" />
              </div>
              <div className={`w-20 h-20 rounded-full flex items-center justify-center text-3xl font-bold text-white shadow-lg ${
                overallScore >= 90 ? 'bg-green-500' :
                overallScore >= 80 ? 'bg-lime-500' :
                overallScore >= 70 ? 'bg-yellow-500' :
                overallScore >= 60 ? 'bg-orange-500' : 'bg-red-500'
              }`}>
                {getScoreGrade(overallScore)}
              </div>
            </div>
            
            {/* Performance indicator */}
            <div className="mb-4">
              <div className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Performance Level
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                <div 
                  className={`h-3 rounded-full transition-all duration-2000 ease-out ${
                    overallScore >= 90 ? 'bg-gradient-to-r from-green-400 to-green-600' :
                    overallScore >= 80 ? 'bg-gradient-to-r from-lime-400 to-lime-600' :
                    overallScore >= 70 ? 'bg-gradient-to-r from-yellow-400 to-yellow-600' :
                    overallScore >= 60 ? 'bg-gradient-to-r from-orange-400 to-orange-600' : 
                    'bg-gradient-to-r from-red-400 to-red-600'
                  }`}
                  style={{ width: `${overallScore}%` }}
                />
              </div>
            </div>
            
            <p className="text-sm text-gray-600 dark:text-gray-400 font-medium">
              {overallScore >= 90 ? '🌟 Exceptional design quality - Industry leading' :
               overallScore >= 80 ? '✅ Strong design with professional standards' :
               overallScore >= 70 ? '👍 Good design foundation with improvement potential' :
               overallScore >= 60 ? '⚠️ Below average design needs focused attention' :
               '🚨 Critical design issues require immediate action'}
            </p>
          </div>
        </div>

        {/* Category Scores */}
        <div>
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Category Breakdown
          </h4>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(scores).map(([category, score]) => {
              const config = categoryConfig[category as keyof ScoresBreakdown];
              if (!config) return null;
              
              return (
                <ScoreCard
                  key={category}
                  category={config.label}
                  score={score}
                  icon={config.icon}
                  description={config.description}
                />
              );
            })}
          </div>
        </div>

      </CardContent>
    </Card>
  );
};

export default ScoreDisplay;
