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
    padding: 25,
    fontFamily: 'Helvetica',
  },
  headerContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 25,
    paddingBottom: 20,
    borderBottom: '3px solid #3b82f6',
    backgroundColor: '#f8fafc',
    padding: 20,
    borderRadius: 8,
  },
  logo: {
    width: 45,
    height: 45,
    marginRight: 18,
  },
  header: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#1e40af',
    letterSpacing: 0.5,
  },
  section: {
    margin: 6,
    padding: 16,
    borderRadius: 8,
    backgroundColor: '#f8fafc',
    border: '1px solid #e2e8f0',
  },
  compactSection: {
    margin: 6,
    padding: 14,
    borderRadius: 8,
    backgroundColor: '#f8fafc',
    border: '1px solid #e2e8f0',
  },
  title: {
    fontSize: 18,
    marginBottom: 12,
    fontWeight: 'bold',
    color: '#1f2937',
    borderBottom: '2px solid #3b82f6',
    paddingBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 15,
    marginBottom: 10,
    fontWeight: 'bold',
    color: '#374151',
    marginTop: 12,
  },
  text: {
    fontSize: 12,
    lineHeight: 1.5,
    color: '#4b5563',
    marginBottom: 6,
    paddingLeft: 10,
  },
  score: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#059669',
    textAlign: 'center',
    marginVertical: 20,
    padding: 20,
    backgroundColor: '#f0fdf4',
    borderRadius: 10,
    border: '2px solid #10b981',
  },
  url: {
    fontSize: 14,
    color: '#3b82f6',
    marginBottom: 15,
    textAlign: 'center',
    fontWeight: 'bold',
    backgroundColor: '#eff6ff',
    padding: 8,
    borderRadius: 6,
  },
  footer: {
    position: 'absolute',
    bottom: 20,
    left: 25,
    right: 25,
    textAlign: 'center',
    fontSize: 10,
    color: '#6b7280',
    borderTop: '2px solid #e5e7eb',
    paddingTop: 10,
    backgroundColor: '#f9fafb',
    padding: 12,
    borderRadius: 6,
  },
  scoreBreakdown: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginVertical: 15,
    padding: 18,
    backgroundColor: '#f1f5f9',
    borderRadius: 10,
    border: '1px solid #cbd5e1',
  },
  scoreItem: {
    width: '25%',
    textAlign: 'center',
    marginBottom: 10,
    padding: 8,
  },
  scoreItemTitle: {
    fontSize: 10,
    color: '#64748b',
    marginBottom: 4,
    fontWeight: 'bold',
  },
  scoreItemValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1e293b',
  },
  issueItem: {
    flexDirection: 'row',
    marginBottom: 6,
    paddingLeft: 12,
    alignItems: 'flex-start',
  },
  bullet: {
    width: 4,
    height: 4,
    borderRadius: 2,
    backgroundColor: '#ef4444',
    marginRight: 8,
    marginTop: 6,
  },
  recommendationBullet: {
    width: 4,
    height: 4,
    borderRadius: 2,
    backgroundColor: '#10b981',
    marginRight: 8,
    marginTop: 6,
  },
  strengthsSection: {
    backgroundColor: '#f0fdf4',
    padding: 16,
    marginBottom: 12,
    borderRadius: 8,
    border: '2px solid #22c55e',
  },
  improvementsSection: {
    backgroundColor: '#fef2f2',
    padding: 16,
    marginBottom: 12,
    borderRadius: 8,
    border: '2px solid #ef4444',
  },
  aiAnalysisSection: {
    backgroundColor: '#faf5ff',
    padding: 20,
    marginBottom: 15,
    borderRadius: 10,
    border: '2px solid #8b5cf6',
    flex: 1,
    minHeight: 550,
  },
  llmContent: {
    fontSize: 11,
    lineHeight: 1.7,
    color: '#374151',
    marginTop: 10,
    textAlign: 'justify',
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
    backgroundColor: '#f1f5f9',
    padding: 10,
    borderRadius: 6,
  },
  infoItem: {
    fontSize: 11,
    color: '#475569',
    textAlign: 'center',
    fontWeight: 'bold',
  },
  gradeCircle: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: '#10b981',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 8,
    alignSelf: 'center',
  },
  gradeText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  summaryCard: {
    backgroundColor: '#ffffff',
    padding: 18,
    marginBottom: 15,
    borderRadius: 10,
    border: '2px solid #e2e8f0',
  },
  categoryHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    paddingBottom: 8,
    borderBottom: '1px solid #e2e8f0',
  },
  categoryIcon: {
    fontSize: 16,
    marginRight: 8,
  },
  categoryTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1e293b',
    flex: 1,
  },
  categoryScore: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#059669',
  },
  divider: {
    height: 2,
    backgroundColor: '#e2e8f0',
    marginVertical: 15,
  },
});

// Helper function to format category names
const formatCategoryName = (category: string): string => {
  return category.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ');
};

// New API Document Component - Enhanced for Multi-Page Reports
const NewReportDocument: React.FC<{ data: AnalysisResponse }> = ({ data }) => {
  
  // Helper function to split long content into manageable chunks for PDF pages
  const splitContentForPages = (content: string, maxLength: number = 3500) => {
    if (!content || content.length <= maxLength) return [content || 'No content available'];
    
    const chunks = [];
    let currentChunk = '';
    
    // Split by sentences first, preserving punctuation and spacing
    const sentences = content.match(/[^.!?]*[.!?]*\s*/g) || [content];
    
    for (const sentence of sentences) {
      if (!sentence.trim()) continue; // Skip empty sentences
      
      // If adding this sentence would exceed the limit and we have content
      if ((currentChunk + sentence).length > maxLength && currentChunk.length > 0) {
        chunks.push(currentChunk.trim());
        currentChunk = sentence;
      } else {
        currentChunk += sentence;
      }
    }
    
    // Always add the remaining content
    if (currentChunk.trim()) {
      chunks.push(currentChunk.trim());
    }
    
    // Ensure we return at least one chunk with content
    if (chunks.length === 0) {
      chunks.push(content);
    }
    
    return chunks;
  };

  const aiAnalysisChunks = data.ai_insights?.llm_analysis?.content 
    ? splitContentForPages(data.ai_insights.llm_analysis.content)
    : ['No AI analysis content available'];

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
      {/* First Page - Executive Summary */}
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
            <Text style={styles.infoItem}>
              Duration: {data.analysis_duration.toFixed(1)}s
            </Text>
          </View>
        </View>

        {/* Overall Score with Enhanced Design */}
        <View style={[styles.score, { alignItems: 'center' }]}>
          <Text style={{ fontSize: 14, color: '#047857', marginBottom: 8, fontWeight: 'bold' }}>
            OVERALL DESIGN SCORE
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
            {data.overall_score >= 90 ? 'EXCELLENT - Outstanding design quality' :
             data.overall_score >= 80 ? 'GOOD - Strong design with minor improvements' :
             data.overall_score >= 70 ? 'FAIR - Decent design with room for enhancement' :
             data.overall_score >= 60 ? 'POOR - Needs significant improvements' :
             'CRITICAL - Major design issues require attention'}
          </Text>
        </View>

        {/* Enhanced Score Breakdown */}
        <View style={styles.scoreBreakdown}>
          <Text style={[styles.subtitle, { textAlign: 'center', color: '#1e293b', marginBottom: 15, fontSize: 16 }]}>
            CATEGORY PERFORMANCE
          </Text>
          {Object.entries(data.scores_breakdown).map(([category, score]) => (
            <View key={category} style={styles.scoreItem}>
              <Text style={styles.scoreItemTitle}>
                {formatCategoryName(category).toUpperCase()}
              </Text>
              <Text style={[styles.scoreItemValue, { color: getScoreGradeColor(score) }]}>
                {score}/100
              </Text>
              <Text style={{ fontSize: 14, fontWeight: 'bold', color: '#64748b', marginTop: 2 }}>
                {getGrade(score)}
              </Text>
            </View>
          ))}
        </View>

        {/* Key Strengths Section */}
        <View style={styles.strengthsSection}>
          <View style={styles.categoryHeader}>
            <Text style={styles.categoryIcon}>✅</Text>
            <Text style={[styles.categoryTitle, { color: '#065f46' }]}>KEY STRENGTHS</Text>
          </View>
          {data.ai_insights?.report_summary?.strengths?.slice(0, 4).map((strength: string, index: number) => (
            <View key={index} style={styles.issueItem}>
              <View style={[styles.recommendationBullet]} />
              <Text style={[styles.text, { flex: 1, fontSize: 11 }]}>{strength}</Text>
            </View>
          )) || (
            <Text style={styles.text}>No strengths data available</Text>
          )}
        </View>


        <Text style={styles.footer}>
          🤖 AI-Powered Website Design Analysis • Generated by Web Engine • {new Date().toLocaleDateString()} • Page 1
        </Text>
      </Page>

      {/* Additional Pages for Detailed AI Analysis */}
      {aiAnalysisChunks.map((chunk, pageIndex) => (
        <Page key={pageIndex} size="A4" style={styles.page}>
          {/* Header for analysis pages */}
          <View style={[styles.headerContainer, { marginBottom: 20 }]}>
            <Text style={[styles.header, { fontSize: 20 }]}>
              AI Analysis {aiAnalysisChunks.length > 1 ? `(Part ${pageIndex + 1})` : ''}
            </Text>
          </View>
          
          <View style={styles.aiAnalysisSection}>
            <View style={styles.categoryHeader}>
              <Text style={styles.categoryTitle}>PROFESSIONAL DESIGN ASSESSMENT</Text>
            </View>
            
            {pageIndex === 0 && data.ai_insights?.llm_analysis && (
              <View style={styles.infoRow}>
                <Text style={styles.infoItem}>
                  Model: {data.ai_insights.llm_analysis.model_used || 'AI Vision Analysis'}
                </Text>
                {data.ai_insights.llm_analysis.confidence_score && (
                  <Text style={styles.infoItem}>
                    Confidence: {Math.round(data.ai_insights.llm_analysis.confidence_score * 100)}%
                  </Text>
                )}
                {!data.ai_insights.llm_analysis.confidence_score && (
                  <Text style={styles.infoItem}>
                    Analysis: Vision-based Assessment
                  </Text>
                )}
              </View>
            )}
            
            <View style={styles.divider} />
            
            <Text style={styles.llmContent}>
              {chunk ? 
                chunk.replace(/\*\*(.*?)\*\*/g, '$1').replace(/#{1,6}\s/g, '').trim() : 
                'No content available for this page.'
              }
            </Text>
          </View>

          <Text style={styles.footer}>
            🤖 AI-Powered Website Design Analysis • Generated by Web Engine • {new Date().toLocaleDateString()} • Page {pageIndex + 2}
          </Text>
        </Page>
      ))}
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

  // Simple fallback handler for when PDF renderer fails
  const handleDownloadClick = () => {
    try {
      // Create a simple text version as fallback
      const reportData = isNewFormat ? data as AnalysisResponse : data as ReportData;
      const textContent = isNewFormat ? 
        `Website Design Analysis Report
URL: ${reportData.url}
Overall Score: ${(reportData as AnalysisResponse).overall_score}/100
Analysis Date: ${new Date((reportData as AnalysisResponse).completed_at).toLocaleString()}

AI Analysis Content:
${(reportData as AnalysisResponse).ai_insights?.llm_analysis?.content || 'No analysis content available'}
` : 
        `Website Design Report
URL: ${reportData.url}
Overall Score: ${(reportData as ReportData).overallScore}/100
Generated: ${(reportData as ReportData).timestamp.toLocaleString()}
`;

      const blob = new Blob([textContent], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `website-report-${Date.now()}.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download fallback failed:', error);
    }
  };

  return (
    <div className="flex flex-col gap-2">
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
                PDF Error - Use Text Version
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
      
      {/* Fallback text download button */}
      <Button 
        onClick={handleDownloadClick}
        variant="outline" 
        size="sm"
        className="text-xs"
      >
        📄 Download as Text (Fallback)
      </Button>
    </div>
  );
};

// Export both data types for backward compatibility
export type { ReportData, AnalysisResponse };
