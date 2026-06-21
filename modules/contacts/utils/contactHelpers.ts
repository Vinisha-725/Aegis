// Helper utilities for contact operations

import type { Contact } from "../types/contact.types"

/**
 * Format wallet address for display (truncate middle)
 */
export function formatWalletAddress(address: string, chars: number = 6): string {
  if (!address || address.length <= chars * 2) {
    return address
  }
  return `${address.slice(0, chars)}...${address.slice(-chars)}`
}

/**
 * Filter contacts by search term (name or wallet address)
 */
export function filterContacts(contacts: Contact[], searchTerm: string): Contact[] {
  if (!searchTerm.trim()) {
    return contacts
  }

  const term = searchTerm.toLowerCase()
  return contacts.filter(
    (contact) =>
      contact.name.toLowerCase().includes(term) ||
      contact.walletAddress.toLowerCase().includes(term)
  )
}

/**
 * Sort contacts by reputation score (highest first)
 */
export function sortByReputation(contacts: Contact[]): Contact[] {
  return [...contacts].sort((a, b) => {
    const scoreA = a.reputationScore ?? 0
    const scoreB = b.reputationScore ?? 0
    return scoreB - scoreA
  })
}

/**
 * Sort contacts by creation date (newest first)
 */
export function sortByCreatedAt(contacts: Contact[]): Contact[] {
  return [...contacts].sort((a, b) => {
    const dateA = a.createdAt ? new Date(a.createdAt).getTime() : 0
    const dateB = b.createdAt ? new Date(b.createdAt).getTime() : 0
    return dateB - dateA
  })
}

/**
 * Get reputation color based on score
 */
export function getReputationColor(score: number): string {
  if (score >= 80) return "text-green-400"
  if (score >= 60) return "text-yellow-400"
  if (score >= 40) return "text-orange-400"
  return "text-red-400"
}
