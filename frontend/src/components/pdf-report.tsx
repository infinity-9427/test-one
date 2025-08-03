'use client'

import React from 'react';
import { Document, Page, Text, View, StyleSheet, PDFDownloadLink, Image } from '@react-pdf/renderer';
import { Button } from '@/components/ui/button';
import { AnalysisResponse } from '@/lib/api-client';

// Create styles for the PDF
const styles = StyleSheet.create({
  page: {
    flexDirection: 'column',
    backgroundColor: '#ffffff',
    padding: 30,
    fontFamily: 'Helvetica',
  },
  headerContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
    paddingBottom: 15,
    borderBottom: '2px solid #e5e7eb',
  },
  logo: {
    width: 40,
    height: 40,
    marginRight: 15,
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1e40af',
    letterSpacing: 0.5,
  },
  section: {
    margin: 8,
    padding: 12,
    borderRadius: 6,
    backgroundColor: '#f8fafc',
  },
  compactSection: {
    margin: 6,
    padding: 10,
    borderRadius: 6,
    backgroundColor: '#f8fafc',
  },
  title: {
    fontSize: 16,
    marginBottom: 8,
    fontWeight: 'bold',
    color: '#1f2937',
    borderBottom: '1px solid #e5e7eb',
    paddingBottom: 6,
  },
  subtitle: {
    fontSize: 14,
    marginBottom: 8,
    fontWeight: 'bold',
    color: '#374151',
    marginTop: 8,
  },
  text: {
    fontSize: 11,
    lineHeight: 1.4,
    color: '#4b5563',
    marginBottom: 4,
    paddingLeft: 8,
  },
  score: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#059669',
    textAlign: 'center',
    marginVertical: 15,
    padding: 12,
    backgroundColor: '#f0fdf4',
    borderRadius: 6,
  },
  url: {
    fontSize: 12,
    color: '#3b82f6',
    marginBottom: 12,
    textAlign: 'center',
    fontWeight: 'bold',
  },
  footer: {
    position: 'absolute',
    bottom: 25,
    left: 30,
    right: 30,
    textAlign: 'center',
    fontSize: 9,
    color: '#6b7280',
    borderTop: '1px solid #e5e7eb',
    paddingTop: 8,
  },
  scoreBreakdown: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginVertical: 12,
    padding: 12,
    backgroundColor: '#f8fafc',
    borderRadius: 6,
  },
  scoreItem: {
    width: '25%',
    textAlign: 'center',
    marginBottom: 6,
  },
  scoreItemTitle: {
    fontSize: 9,
    color: '#6b7280',
    marginBottom: 3,
  },
  scoreItemValue: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#1f2937',
  },
  issueItem: {
    flexDirection: 'row',
    marginBottom: 4,
    paddingLeft: 8,
  },
  bullet: {
    width: 3,
    height: 3,
    borderRadius: 2,
    backgroundColor: '#ef4444',
    marginRight: 6,
    marginTop: 5,
  },
  recommendationBullet: {
    width: 3,
    height: 3,
    borderRadius: 2,
    backgroundColor: '#10b981',
    marginRight: 6,
    marginTop: 5,
  },
  strengthsSection: {
    backgroundColor: '#f0fdf4',
    padding: 10,
    marginBottom: 10,
    borderRadius: 6,
  },
  improvementsSection: {
    backgroundColor: '#fef3f2',
    padding: 10,
    marginBottom: 10,
    borderRadius: 6,
  },
  aiAnalysisSection: {
    backgroundColor: '#f8f4ff',
    padding: 10,
    marginBottom: 10,
    borderRadius: 6,
  },
  llmContent: {
    fontSize: 10,
    lineHeight: 1.4,
    color: '#4b5563',
    marginTop: 6,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  infoItem: {
    fontSize: 10,
    color: '#6b7280',
    textAlign: 'center',
  },
});

// Helper function to format category names
const formatCategoryName = (category: string): string => {
  return category.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ');
};

// New API Document Component
const NewReportDocument: React.FC<{ data: AnalysisResponse }> = ({ data }) => (
  <Document>
    <Page size="A4" style={styles.page}>
      {/* Header with Logo */}
      <View style={styles.headerContainer}>
        <Image style={styles.logo} src="/logo-web-engine.png" />
        <Text style={styles.header}>Website Design Analysis Report</Text>
      </View>
      
      {/* URL and Basic Info */}
      <View style={styles.compactSection}>
        <Text style={styles.url}>{data.url}</Text>
        <View style={styles.infoRow}>
          <Text style={styles.infoItem}>
            Completed: {new Date(data.completed_at).toLocaleDateString()}
          </Text>
          <Text style={styles.infoItem}>
            Time: {new Date(data.completed_at).toLocaleTimeString()}
          </Text>
          <Text style={styles.infoItem}>
            Duration: {data.analysis_duration.toFixed(1)}s
          </Text>
        </View>
      </View>

      {/* Overall Score */}
      <View style={styles.score}>
        <Text style={{ fontSize: 12, color: '#6b7280', marginBottom: 6 }}>Overall Design Score</Text>
        <Text style={{ fontSize: 28, fontWeight: 'bold', color: '#059669' }}>{data.overall_score}/100</Text>
      </View>

      {/* Score Breakdown */}
      <View style={styles.scoreBreakdown}>
        {Object.entries(data.scores_breakdown).map(([category, score]) => (
          <View key={category} style={styles.scoreItem}>
            <Text style={styles.scoreItemTitle}>{formatCategoryName(category)}</Text>
            <Text style={styles.scoreItemValue}>{score}/100</Text>
          </View>
        ))}
      </View>

      {/* Executive Summary - Strengths */}
      <View style={styles.strengthsSection}>
        <Text style={[styles.title, { color: '#065f46' }]}>Key Strengths</Text>
        {data.ai_insights?.report_summary?.strengths?.slice(0, 4).map((strength: string, index: number) => (
          <View key={index} style={styles.issueItem}>
            <View style={[styles.recommendationBullet]} />
            <Text style={[styles.text, { flex: 1 }]}>{strength}</Text>
          </View>
        )) || (
          <Text style={styles.text}>No strengths data available</Text>
        )}
      </View>

      {/* Areas for Improvement */}
      {data.ai_insights?.report_summary?.improvement_areas && (
        <View style={styles.improvementsSection}>
          <Text style={[styles.title, { color: '#991b1b' }]}>Areas for Improvement</Text>
          {data.ai_insights.report_summary.improvement_areas.slice(0, 4).map((improvement: string, index: number) => (
            <View key={index} style={styles.issueItem}>
              <View style={[styles.bullet]} />
              <Text style={[styles.text, { flex: 1 }]}>{improvement}</Text>
            </View>
          ))}
        </View>
      )}

      {/* AI Analysis - Condensed */}
      <View style={styles.aiAnalysisSection}>
        <Text style={styles.title}>AI Visual Analysis Summary</Text>
        <View style={styles.infoRow}>
          <Text style={styles.infoItem}>Model: {data.ai_insights.llm_analysis.model_used}</Text>
          <Text style={styles.infoItem}>
            Confidence: {Math.round(data.ai_insights.llm_analysis.confidence_score * 100)}%
          </Text>
        </View>
        <Text style={[styles.llmContent, { marginTop: 8 }]}>
          {data.ai_insights.llm_analysis.content.length > 800 
            ? data.ai_insights.llm_analysis.content.substring(0, 800) + '...'
            : data.ai_insights.llm_analysis.content
          }
        </Text>
      </View>

      <Text style={styles.footer}>
        AI-Powered Website Design Analysis • Generated by Web Engine • {new Date().toLocaleDateString()}
      </Text>
    </Page>
  </Document>
);

// Legacy interface for backward compatibility
interface ReportData {
  url: string;
  overallScore: number;
  typography: {
    score: number;
    issues: string[];
    recommendations: string[];
  };
  color: {
    score: number;
    issues: string[];
    recommendations: string[];
  };
  layout: {
    score: number;
    issues: string[];
    recommendations: string[];
  };
  timestamp: Date;
}

// Legacy PDF Document Component
const LegacyReportDocument: React.FC<{ data: ReportData }> = ({ data }) => (
  <Document>
    <Page size="A4" style={styles.page}>
      {/* Header with Logo */}
      <View style={styles.headerContainer}>
        <Image style={styles.logo} src="/logo-web-engine.png" />
        <Text style={styles.header}>Website Design Scoring Report</Text>
      </View>
      
      <View style={styles.compactSection}>
        <Text style={styles.url}>{data.url}</Text>
        <Text style={[styles.infoItem, { textAlign: 'center' }]}>
          Generated on: {data.timestamp.toLocaleDateString()} at {data.timestamp.toLocaleTimeString()}
        </Text>
      </View>

      <View style={styles.score}>
        <Text style={{ fontSize: 12, color: '#6b7280', marginBottom: 6 }}>Overall Design Score</Text>
        <Text style={{ fontSize: 28, fontWeight: 'bold', color: '#059669' }}>{data.overallScore}/100</Text>
      </View>

      {/* Legacy score breakdown */}
      <View style={styles.scoreBreakdown}>
        <View style={styles.scoreItem}>
          <Text style={styles.scoreItemTitle}>Typography</Text>
          <Text style={[styles.scoreItemValue, { color: '#3b82f6' }]}>{data.typography.score}/100</Text>
        </View>
        <View style={styles.scoreItem}>
          <Text style={styles.scoreItemTitle}>Color & Accessibility</Text>
          <Text style={[styles.scoreItemValue, { color: '#8b5cf6' }]}>{data.color.score}/100</Text>
        </View>
        <View style={styles.scoreItem}>
          <Text style={styles.scoreItemTitle}>Layout & Structure</Text>
          <Text style={[styles.scoreItemValue, { color: '#f59e0b' }]}>{data.layout.score}/100</Text>
        </View>
      </View>

      {/* Typography Analysis */}
      <View style={styles.strengthsSection}>
        <Text style={styles.title}>Typography Analysis</Text>
        {data.typography.issues.length > 0 && (
          <View>
            <Text style={[styles.subtitle, { color: '#991b1b' }]}>Issues:</Text>
            {data.typography.issues.slice(0, 3).map((issue: string, index: number) => (
              <View key={index} style={styles.issueItem}>
                <View style={styles.bullet} />
                <Text style={[styles.text, { flex: 1 }]}>{issue}</Text>
              </View>
            ))}
          </View>
        )}
        {data.typography.recommendations.length > 0 && (
          <View style={{ marginTop: 8 }}>
            <Text style={[styles.subtitle, { color: '#065f46' }]}>Recommendations:</Text>
            {data.typography.recommendations.slice(0, 2).map((rec: string, index: number) => (
              <View key={index} style={styles.issueItem}>
                <View style={styles.recommendationBullet} />
                <Text style={[styles.text, { flex: 1 }]}>{rec}</Text>
              </View>
            ))}
          </View>
        )}
      </View>

      {/* Color & Layout Analysis */}
      <View style={styles.aiAnalysisSection}>
        <Text style={styles.title}>Color & Layout Analysis</Text>
        <View style={styles.infoRow}>
          <Text style={styles.infoItem}>Color Score: {data.color.score}/100</Text>
          <Text style={styles.infoItem}>Layout Score: {data.layout.score}/100</Text>
        </View>
        {data.color.issues.length > 0 && (
          <Text style={[styles.text, { marginTop: 8 }]}>
            Key Issues: {data.color.issues.slice(0, 2).join(', ')}
          </Text>
        )}
      </View>

      <Text style={styles.footer}>
        Professional Website Design Analysis • Generated by Web Engine • {new Date().toLocaleDateString()}
      </Text>
    </Page>
  </Document>
);

// PDF Download Component that handles both data types
interface PDFReportProps {
  data?: ReportData | AnalysisResponse | null;
  disabled?: boolean;
}

export const PDFReport: React.FC<PDFReportProps> = ({ data, disabled = false }) => {
  if (!data) {
    return (
      <Button disabled variant="outline" size="lg">
        Download PDF Report
      </Button>
    );
  }

  // Check if this is new AnalysisResponse format or legacy ReportData
  const isNewFormat = 'analysis_id' in data;
  
  const getFileName = () => {
    const urlPart = data.url.replace(/https?:\/\//, '').replace(/[^a-zA-Z0-9]/g, '-');
    const timestamp = isNewFormat ? 
      new Date((data as AnalysisResponse).completed_at).getTime() : 
      (data as ReportData).timestamp.getTime();
    return `website-report.pdf`;
  };

  return (
    <PDFDownloadLink
      document={
        isNewFormat ? 
          <NewReportDocument data={data as AnalysisResponse} /> : 
          <LegacyReportDocument data={data as ReportData} />
      }
      fileName={getFileName()}
    >
      {({ loading }) => (
        <Button 
          disabled={loading || disabled} 
          size="lg"
          className="bg-blue-600 hover:bg-blue-700"
        >
          {loading ? (
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
              Generating PDF...
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Download PDF Report
            </div>
          )}
        </Button>
      )}
    </PDFDownloadLink>
  );
};

// Export both data types for backward compatibility
export type { ReportData, AnalysisResponse };
