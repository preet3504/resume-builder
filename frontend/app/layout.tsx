import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

export const metadata: Metadata = {
  title: 'ResumeTailor',
  description: 'Create optimized, ATS-friendly resumes tailored to your target job description',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont/tabler-icons.min.css" />
      </head>
      <body className="min-h-screen bg-bg text-slate-200">{children}</body>
    </html>
  );
}