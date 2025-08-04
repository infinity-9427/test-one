'use client'

import React from 'react';
import { Document, Page, Text, View, StyleSheet, PDFDownloadLink, Image } from '@react-pdf/renderer';
import { Button } from '@/components/ui/button';
import { AnalysisResponse } from '@/lib/api-client';

// Design System Colors - Tailwind-based tokens
const colors = {
  primary: '#2563eb',      // Tailwind: blue-600
  primaryDark: '#1e40af',  // Tailwind: blue-700
  secondary: '#f8fafc',    // Tailwind: slate-50
  accent: '#10b981',       // Tailwind: emerald-500
  accentLight: '#f0fdf4',  // Tailwind: emerald-50
  danger: '#ef4444',       // Tailwind: red-500
  dangerLight: '#fef2f2',  // Tailwind: red-50
  warning: '#f59e0b',      // Tailwind: amber-500
  info: '#3b82f6',         // Tailwind: blue-500
  infoLight: '#eff6ff',    // Tailwind: blue-50
  grayLight: '#f1f5f9',    // Tailwind: slate-100
  gray: '#64748b',         // Tailwind: slate-500
  grayDark: '#1e293b',     // Tailwind: slate-800
  white: '#ffffff',
  black: '#0f172a',        // Tailwind: slate-900
  success: '#22c55e',      // Tailwind: green-500
  purple: '#8b5cf6',       // Tailwind: violet-500
  purpleLight: '#faf5ff',  // Tailwind: violet-50
  border: '#e2e8f0',       // Tailwind: slate-200
  borderLight: '#cbd5e1',  // Tailwind: slate-300
};

// Reusable style patterns
const cardBase = {
  padding: 18,
  borderRadius: 10,
  backgroundColor: colors.white,
  border: `2px solid ${colors.border}`,
  marginBottom: 15,
};

const sectionBase = {
  padding: 16,
  borderRadius: 8,
  marginBottom: 12,
};

// Typography scale
const typography = {
  h1: { fontSize: 28, fontWeight: 'bold', lineHeight: 1.2 },
  h2: { fontSize: 20, fontWeight: 'bold', lineHeight: 1.3 },
  h3: { fontSize: 16, fontWeight: 'bold', lineHeight: 1.4 },
  body: { fontSize: 12, lineHeight: 1.6 },
  small: { fontSize: 10, lineHeight: 1.5 },
  large: { fontSize: 14, lineHeight: 1.5 },
};

// Create styles for the PDF
const styles = StyleSheet.create({
  page: {
    flexDirection: 'column',
    backgroundColor: colors.secondary,
    padding: 36,
    fontFamily: 'Helvetica',
  },
  headerContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 32,
    paddingBottom: 24,
    borderBottom: `4px solid ${colors.primary}`,
    backgroundColor: colors.grayLight,
    padding: 24,
    borderRadius: 12,
  },
  logo: {
    width: 48,
    height: 48,
    marginRight: 20,
  },
  header: {
    ...typography.h1,
    color: colors.primaryDark,
    letterSpacing: 0.5,
  },
  section: {
    ...sectionBase,
    backgroundColor: colors.secondary,
    border: `1px solid ${colors.border}`,
  },
  compactSection: {
    ...sectionBase,
    padding: 14,
    backgroundColor: colors.secondary,
    border: `1px solid ${colors.border}`,
  },
  title: {
    ...typography.h2,
    marginBottom: 12,
    color: colors.grayDark,
    borderBottom: `2px solid ${colors.primary}`,
    paddingBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    ...typography.h3,
    marginBottom: 10,
    color: colors.gray,
    marginTop: 12,
  },
  text: {
    ...typography.body,
    color: colors.gray,
    marginBottom: 6,
    paddingLeft: 10,
  },
  score: {
    fontSize: 22,
    fontWeight: 'bold',
    color: colors.accent,
    textAlign: 'center',
    marginVertical: 20,
    padding: 24,
    backgroundColor: colors.accentLight,
    borderRadius: 12,
    border: `2px solid ${colors.accent}`,
  },
  url: {
    ...typography.large,
    color: colors.info,
    marginBottom: 15,
    textAlign: 'center',
    fontWeight: 'bold',
    backgroundColor: colors.infoLight,
    padding: 12,
    borderRadius: 8,
  },
  footer: {
    textAlign: 'center',
    ...typography.small,
    color: colors.gray,
    borderTop: `2px solid ${colors.border}`,
    paddingTop: 12,
    backgroundColor: colors.grayLight,
    padding: 15,
    borderRadius: 8,
    marginTop: 20,
  },
  scoreBreakdown: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginVertical: 20,
    padding: 22,
    backgroundColor: colors.grayLight,
    borderRadius: 12,
    border: `2px solid ${colors.borderLight}`,
  },
  scoreItem: {
    width: '25%',
    textAlign: 'center',
    marginBottom: 12,
    padding: 10,
  },
  scoreItemTitle: {
    ...typography.small,
    color: colors.gray,
    marginBottom: 6,
    fontWeight: 'bold',
  },
  scoreItemValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.grayDark,
  },
  issueItem: {
    flexDirection: 'row',
    marginBottom: 8,
    paddingLeft: 15,
    alignItems: 'flex-start',
  },
  bullet: {
    width: 5,
    height: 5,
    borderRadius: 2.5,
    backgroundColor: colors.danger,
    marginRight: 10,
    marginTop: 7,
  },
  recommendationBullet: {
    width: 5,
    height: 5,
    borderRadius: 2.5,
    backgroundColor: colors.accent,
    marginRight: 10,
    marginTop: 7,
  },
  strengthsSection: {
    backgroundColor: colors.accentLight,
    padding: 20,
    marginBottom: 15,
    borderRadius: 10,
    border: `2px solid ${colors.success}`,
  },
  improvementsSection: {
    backgroundColor: colors.dangerLight,
    padding: 20,
    marginBottom: 15,
    borderRadius: 10,
    border: `2px solid ${colors.danger}`,
  },
  aiAnalysisSection: {
    backgroundColor: colors.purpleLight,
    padding: 20,
    marginBottom: 15,
    borderRadius: 12,
    border: `2px solid ${colors.purple}`,
  },
  llmContent: {
    fontSize: 11,
    lineHeight: 1.8,
    color: colors.grayDark,
    marginTop: 12,
    textAlign: 'justify',
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
    backgroundColor: colors.grayLight,
    padding: 12,
    borderRadius: 8,
  },
  infoItem: {
    fontSize: 11,
    color: colors.gray,
    textAlign: 'center',
    fontWeight: 'bold',
  },
  gradeCircle: {
    width: 52,
    height: 52,
    borderRadius: 26,
    backgroundColor: colors.accent,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 10,
    alignSelf: 'center',
  },
  gradeText: {
    fontSize: 26,
    fontWeight: 'bold',
    color: colors.white,
  },
  summaryCard: {
    ...cardBase,
    backgroundColor: colors.white,
    padding: 20,
    marginBottom: 18,
    borderRadius: 12,
    border: `2px solid ${colors.border}`,
  },
  categoryHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
    paddingBottom: 10,
    borderBottom: `1px solid ${colors.border}`,
  },
  categoryIcon: {
    fontSize: 18,
    marginRight: 10,
  },
  categoryTitle: {
    ...typography.h3,
    color: colors.grayDark,
    flex: 1,
  },
  categoryScore: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.accent,
  },
  divider: {
    height: 2,
    backgroundColor: colors.border,
    marginVertical: 18,
  },
});

// Helper function to format category names
const formatCategoryName = (category: string): string => {
  return category.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ');
};

// New API Document Component - Professional Single-Page Layout
const NewReportDocument: React.FC<{ data: AnalysisResponse }> = ({ data }) => {
  
  // Format AI analysis content for professional display
  const formatAnalysisContent = (content: string): string => {
    if (!content) return 'No AI analysis content available';
    
    // Clean up markdown and format for PDF
    return content
      .replace(/\*\*(.*?)\*\*/g, '$1') // Remove bold markdown
      .replace(/#{1,6}\s/g, '') // Remove header markdown
      .replace(/\n{3,}/g, '\n\n') // Normalize multiple line breaks
      .trim();
  };

  const analysisContent = data.ai_insights?.llm_analysis?.content 
    ? formatAnalysisContent(data.ai_insights.llm_analysis.content)
    : 'No AI analysis content available';

  // Helper function to get score color for grade circles
  const getScoreGradeColor = (score: number): string => {
    if (score >= 90) return '#22c55e'; // green
    if (score >= 80) return '#3b82f6'; // blue
    if (score >= 70) return '#f59e0b'; // yellow
    if (score >= 60) return '#f97316'; // orange
    return '#ef4444'; // red
  };

  const getGrade = (score: number): string => {
    if (score >= 90) return 'A';
    if (score >= 80) return 'B';
    if (score >= 70) return 'C';
    if (score >= 60) return 'D';
    return 'F';
  };

  return (
    <Document>
      {/* Single Page - Complete Report */}
      <Page size="A4" style={styles.page}>
        {/* Enhanced Header */}
        <View style={styles.headerContainer}>
          {/* eslint-disable-next-line jsx-a11y/alt-text */}
          <Image style={styles.logo} src="/logo-web-engine.png" />
          <Text style={styles.header}>Website Design Analysis Report</Text>
        </View>
        
        {/* Website Information Card */}
        <View style={styles.summaryCard}>
          <Text style={styles.url}>{data.url}</Text>
          <View style={styles.infoRow}>
            <Text style={styles.infoItem}>
              Completed: {new Date(data.completed_at).toLocaleDateString()}
            </Text>
          </View>
        </View>

        {/* Overall Score with Enhanced Design */}
        <View style={[styles.score, { alignItems: 'center' }]}>
          <Text style={{ fontSize: 14, color: '#047857', marginBottom: 8, fontWeight: 'bold' }}>
            Overall Design Score
          </Text>
          <View style={{ flexDirection: 'row', alignItems: 'center', marginHorizontal: 20 }}>
            <Text style={{ fontSize: 42, fontWeight: 'bold', color: '#059669' }}>
              {data.overall_score}/100
            </Text>
            <View style={[styles.gradeCircle, { backgroundColor: getScoreGradeColor(data.overall_score), marginLeft: 20 }]}>
              <Text style={styles.gradeText}>{getGrade(data.overall_score)}</Text>
            </View>
          </View>
          <Text style={{ fontSize: 12, color: '#065f46', marginTop: 8, textAlign: 'center' }}>
            {data.overall_score >= 90 ? 'Excellent - Outstanding design quality' :
             data.overall_score >= 80 ? 'Good - Strong design with minor improvements' :
             data.overall_score >= 70 ? 'Fair - Decent design with room for enhancement' :
             data.overall_score >= 60 ? 'Poor - Needs significant improvements' :
             'Critical - Major design issues require attention'}
          </Text>
        </View>

        {/* Enhanced Score Breakdown */}
        <View style={styles.section}>
          <Text style={styles.title}>Category Performance</Text>
          {Object.entries(data.scores_breakdown).map(([category, score]) => (
            <View key={category} style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
              <Text style={styles.text}>
                {formatCategoryName(category)}
              </Text>
              <Text style={[styles.text, { fontWeight: 'bold' }]}>
                {score}/100
              </Text>
            </View>
          ))}
        </View>

        {/* Key Strengths Section */}
        <View style={styles.strengthsSection}>
          <Text style={[styles.title, { color: colors.success, backgroundColor: 'transparent', borderBottom: 0, paddingBottom: 4 }]}>
            Key Strengths
          </Text>
          {data.ai_insights?.report_summary?.strengths?.map((strength: string, index: number) => (
            <View key={index} style={styles.issueItem}>
              <View style={[styles.recommendationBullet, { backgroundColor: colors.success }]} />
              <Text style={[styles.text, { marginBottom: 4, paddingLeft: 0, flex: 1 }]}>
                {strength}
              </Text>
            </View>
          )) || (
            <Text style={styles.text}>No strengths data available</Text>
          )}
        </View>


        {/* Complete AI Analysis */}
        <View style={styles.section}>
          <Text style={styles.title}>Professional Design Analysis</Text>
          
          {data.ai_insights?.llm_analysis && (
            <View style={{ marginBottom: 12 }}>
              <Text style={[styles.text, { fontWeight: 'bold' }]}>
                Analysis Model: {data.ai_insights.llm_analysis.model_used || 'AI Vision Analysis'}
              </Text>
              {data.ai_insights.llm_analysis.confidence_score && (
                <Text style={[styles.text, { fontWeight: 'bold' }]}>
                  Confidence Level: {Math.round(data.ai_insights.llm_analysis.confidence_score * 100)}%
                </Text>
              )}
            </View>
          )}
          
          <Text style={[styles.text, { lineHeight: 1.6, textAlign: 'justify' }]}>
            {analysisContent}
          </Text>
        </View>


      </Page>
    </Document>
  );
};

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
        {/* eslint-disable-next-line jsx-a11y/alt-text */}
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
      {({ loading, error }) => (
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
          ) : error ? (
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.728-.833-2.498 0L4.316 15.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              PDF Generation Failed
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

export type { ReportData, AnalysisResponse };
