'use client'

import React from 'react';
import { Document, Page, Text, View, StyleSheet, PDFDownloadLink } from '@react-pdf/renderer';
import { Button } from '@/components/ui/button';

// Create styles for the PDF
const styles = StyleSheet.create({
  page: {
    flexDirection: 'column',
    backgroundColor: '#ffffff',
    padding: 40,
    fontFamily: 'Helvetica',
  },
  header: {
    fontSize: 28,
    marginBottom: 30,
    textAlign: 'center',
    fontWeight: 'bold',
    color: '#1e40af',
    letterSpacing: 0.5,
  },
  section: {
    margin: 12,
    padding: 16,
    borderRadius: 8,
    backgroundColor: '#f8fafc',
  },
  title: {
    fontSize: 20,
    marginBottom: 12,
    fontWeight: 'bold',
    color: '#1f2937',
    borderBottom: '2px solid #e5e7eb',
    paddingBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    marginBottom: 10,
    fontWeight: 'bold',
    color: '#374151',
    marginTop: 12,
  },
  text: {
    fontSize: 12,
    lineHeight: 1.6,
    color: '#4b5563',
    marginBottom: 6,
    paddingLeft: 12,
  },
  score: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#059669',
    textAlign: 'center',
    marginVertical: 20,
    padding: 16,
    backgroundColor: '#f0fdf4',
    borderRadius: 8,
  },
  url: {
    fontSize: 14,
    color: '#3b82f6',
    marginBottom: 20,
    textAlign: 'center',
    fontWeight: 'bold',
  },
  footer: {
    position: 'absolute',
    bottom: 30,
    left: 40,
    right: 40,
    textAlign: 'center',
    fontSize: 10,
    color: '#6b7280',
    borderTop: '1px solid #e5e7eb',
    paddingTop: 12,
  },
  scoreBreakdown: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginVertical: 20,
    padding: 16,
    backgroundColor: '#f8fafc',
    borderRadius: 8,
  },
  scoreItem: {
    textAlign: 'center',
    flex: 1,
  },
  scoreItemTitle: {
    fontSize: 12,
    color: '#6b7280',
    marginBottom: 4,
  },
  scoreItemValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
  },
  issueItem: {
    flexDirection: 'row',
    marginBottom: 6,
    paddingLeft: 12,
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
});

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

// PDF Document Component
const ReportDocument: React.FC<{ data: ReportData }> = ({ data }) => (
  <Document>
    <Page size="A4" style={styles.page}>
      <Text style={styles.header}>Website Design Scoring Report</Text>
      
      <View style={styles.section}>
        <Text style={styles.url}>{data.url}</Text>
        <Text style={[styles.text, { textAlign: 'center', marginBottom: 0 }]}>
          Generated on: {data.timestamp.toLocaleDateString()} at {data.timestamp.toLocaleTimeString()}
        </Text>
      </View>

      <View style={styles.score}>
        <Text style={{ fontSize: 14, color: '#6b7280', marginBottom: 8 }}>Overall Design Score</Text>
        <Text style={{ fontSize: 32, fontWeight: 'bold', color: '#059669' }}>{data.overallScore}/100</Text>
      </View>

      {/* Score Breakdown */}
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

      {/* Typography Section */}
      <View style={styles.section}>
        <Text style={styles.title}>Typography Assessment</Text>
        <Text style={[styles.subtitle, { color: '#3b82f6' }]}>Score: {data.typography.score}/100</Text>
        
        <Text style={styles.subtitle}>Issues Identified:</Text>
        {data.typography.issues.map((issue, index) => (
          <View key={index} style={styles.issueItem}>
            <View style={styles.bullet} />
            <Text style={styles.text}>{issue}</Text>
          </View>
        ))}
        
        <Text style={styles.subtitle}>Recommendations:</Text>
        {data.typography.recommendations.map((rec, index) => (
          <View key={index} style={styles.issueItem}>
            <View style={styles.recommendationBullet} />
            <Text style={styles.text}>{rec}</Text>
          </View>
        ))}
      </View>

      {/* Color Section */}
      <View style={styles.section}>
        <Text style={styles.title}>Color & Accessibility Assessment</Text>
        <Text style={[styles.subtitle, { color: '#8b5cf6' }]}>Score: {data.color.score}/100</Text>
        
        <Text style={styles.subtitle}>Issues Identified:</Text>
        {data.color.issues.map((issue, index) => (
          <View key={index} style={styles.issueItem}>
            <View style={styles.bullet} />
            <Text style={styles.text}>{issue}</Text>
          </View>
        ))}
        
        <Text style={styles.subtitle}>Recommendations:</Text>
        {data.color.recommendations.map((rec, index) => (
          <View key={index} style={styles.issueItem}>
            <View style={styles.recommendationBullet} />
            <Text style={styles.text}>{rec}</Text>
          </View>
        ))}
      </View>

      {/* Layout Section */}
      <View style={styles.section}>
        <Text style={styles.title}>Layout & Structure Assessment</Text>
        <Text style={[styles.subtitle, { color: '#f59e0b' }]}>Score: {data.layout.score}/100</Text>
        
        <Text style={styles.subtitle}>Issues Identified:</Text>
        {data.layout.issues.map((issue, index) => (
          <View key={index} style={styles.issueItem}>
            <View style={styles.bullet} />
            <Text style={styles.text}>{issue}</Text>
          </View>
        ))}
        
        <Text style={styles.subtitle}>Recommendations:</Text>
        {data.layout.recommendations.map((rec, index) => (
          <View key={index} style={styles.issueItem}>
            <View style={styles.recommendationBullet} />
            <Text style={styles.text}>{rec}</Text>
          </View>
        ))}
      </View>

      <Text style={styles.footer}>
        Professional Website Design Analysis Report • Generated by AI-Powered Design Scoring Tool
      </Text>
    </Page>
  </Document>
);

// PDF Download Component
interface PDFReportProps {
  data: ReportData | null;
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

  return (
    <PDFDownloadLink
      document={<ReportDocument data={data} />}
      fileName={`design-report-${data.url.replace(/https?:\/\//, '').replace(/[^a-zA-Z0-9]/g, '-')}-${Date.now()}.pdf`}
    >
      {({ blob, url, loading, error }) => (
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

// Export the ReportData type for use in other components
export type { ReportData };
