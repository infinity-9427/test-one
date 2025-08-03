'use client'

import { useState, useCallback } from 'react';
import { AnalysisResponse, analyzeWebsiteAction, getHealthStatusAction } from '@/lib/api-client';

interface AnalysisState {
  isLoading: boolean;
  isAnalyzing: boolean;
  analysisProgress: number;
  currentAnalysis: AnalysisResponse | null;
  error: string | null;
  analysisHistory: AnalysisResponse[];
  backendHealth: {
    status: 'unknown' | 'healthy' | 'unhealthy';
    lastChecked: Date | null;
  };
}

interface AnalysisOptions {
  autoLogToSheets?: boolean;
  includeMobile?: boolean;
}

const initialState: AnalysisState = {
  isLoading: false,
  isAnalyzing: false,
  analysisProgress: 0,
  currentAnalysis: null,
  error: null,
  analysisHistory: [],
  backendHealth: {
    status: 'unknown',
    lastChecked: null,
  },
};

export const useAnalysis = () => {
  const [state, setState] = useState<AnalysisState>(initialState);

  const setError = useCallback((error: string | null) => {
    setState(prev => ({ ...prev, error, isAnalyzing: false, isLoading: false }));
  }, []);

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  const resetAnalysis = useCallback(() => {
    setState(prev => ({ 
      ...prev, 
      currentAnalysis: null, 
      error: null, 
      isAnalyzing: false,
      analysisProgress: 0 
    }));
  }, []);

  const checkBackendHealth = useCallback(async () => {
    try {
      const result = await getHealthStatusAction();
      setState(prev => ({
        ...prev,
        backendHealth: {
          status: result.success ? 'healthy' : 'unhealthy',
          lastChecked: new Date(),
        },
      }));
      return result.success;
    } catch {
      setState(prev => ({
        ...prev,
        backendHealth: {
          status: 'unhealthy',
          lastChecked: new Date(),
        },
      }));
      return false;
    }
  }, []);

  const analyzeWebsite = useCallback(async (
    url: string, 
    options: AnalysisOptions = {}
  ) => {
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }

    // Clear previous state
    clearError();
    setState(prev => ({ 
      ...prev, 
      isAnalyzing: true, 
      analysisProgress: 0,
      currentAnalysis: null 
    }));

    try {
      // Simulate progress updates (since we don't have real-time progress from backend)
      const progressInterval = setInterval(() => {
        setState(prev => ({
          ...prev,
          analysisProgress: Math.min(prev.analysisProgress + Math.random() * 15, 90)
        }));
      }, 2000);

      // Prepare form data for server action
      const formData = new FormData();
      formData.append('url', url);
      formData.append('autoLogToSheets', String(options.autoLogToSheets ?? true));
      formData.append('includeMobile', String(options.includeMobile ?? true));

      // Call server action
      const result = await analyzeWebsiteAction(formData);

      clearInterval(progressInterval);

      if (!result.success) {
        setError(result.error || 'Analysis failed');
        return;
      }

      // Complete progress and set result
      setState(prev => ({
        ...prev,
        currentAnalysis: result.data!,
        isAnalyzing: false,
        analysisProgress: 100,
        analysisHistory: [result.data!, ...prev.analysisHistory.slice(0, 9)], // Keep last 10
      }));

    } catch (error) {
      console.error('Analysis error:', error);
      setError(
        error instanceof Error 
          ? error.message 
          : 'An unexpected error occurred during analysis'
      );
    }
  }, [setError, clearError]);

  return {
    ...state,
    analyzeWebsite,
    setError,
    clearError,
    resetAnalysis,
    checkBackendHealth,
  };
};
