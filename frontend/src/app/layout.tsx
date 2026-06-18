import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Aegis — AI-Powered Trust Protocol",
  description:
    "Aegis verifies software development milestones using AI agents and automatically releases escrowed payments upon consensus approval.",
  keywords: ["Aegis", "AI verification", "escrow", "blockchain", "trust protocol", "milestones"],
  authors: [{ name: "Aegis" }],
  openGraph: {
    title: "Aegis — AI-Powered Trust Protocol",
    description:
      "AI-powered trust protocol that verifies software milestones and releases escrowed payments.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${jetbrainsMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-slate-950 text-slate-50">
        {children}
      </body>
    </html>
  );
}
