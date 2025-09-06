'use client'

import { AppProvider } from '@/lib/context';
import { AppContent } from '@/components/AppContent';

export default function Home() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

