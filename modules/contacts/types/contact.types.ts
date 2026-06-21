// Contact types for Aegis Protocol
// This module will support freelancer/client identity mapping, wallet address book, reputation linking

export type ContactRole = "client" | "freelancer"

export interface Contact {
  id: string
  name: string
  walletAddress: string
  role: ContactRole
  reputationScore?: number
  createdAt?: string
  notes?: string
}

export interface ContactFormData {
  name: string
  walletAddress: string
  role: ContactRole
  reputationScore?: number
  notes?: string
}
