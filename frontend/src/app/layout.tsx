import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Design Scoring & Reporting Tool",
  description: "Analyze any website's design with our AI-powered assessment tool. Get comprehensive reports on typography, color accessibility, and layout structure with professional recommendations.",
  keywords: ["website design", "design analysis", "UI/UX", "accessibility", "typography", "AI analysis", "design scoring"],
  authors: [{ name: "Jorge Tarifa" }],
  creator: "Jorge Tarifa",
  publisher: "Jorge Tarifa",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL(process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: "Design Scoring & Reporting Tool",
    description: "Analyze any website's design with our AI-powered assessment tool. Get comprehensive reports on typography, color accessibility, and layout structure.",
    url: '/',
    siteName: 'Design Scoring Tool',
    images: [
      {
        url: '/logo-web-engine.png',
        width: 800,
        height: 600,
        alt: 'Design Scoring Tool Logo',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: "Design Scoring & Reporting Tool",
    description: "AI-powered website design analysis with professional reports",
    images: ['/logo-web-engine.png'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  icons: {
    icon: '/logo-web-engine.png',
    shortcut: '/logo-web-engine.png',
    apple: '/logo-web-engine.png',
    other: {
      rel: 'apple-touch-icon-precomposed',
      url: '/logo-web-engine.png',
    },
  },
  manifest: '/manifest.json',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${inter.variable} ${jetbrainsMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
