import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "Aegis Protocol – Blockchain Test Console",
  description: "Developer testing dashboard for Solana-based escrow smart contract system",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
