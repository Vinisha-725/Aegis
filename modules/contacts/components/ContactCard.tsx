// Contact card component for displaying individual contact info

import type { Contact } from "../types/contact.types"

interface ContactCardProps {
  contact: Contact
  onSelect?: (contact: Contact) => void
}

export function ContactCard({ contact, onSelect }: ContactCardProps) {
  const getRoleColor = (role: string) => {
    switch (role) {
      case "client":
        return "text-blue-400"
      case "freelancer":
        return "text-green-400"
      default:
        return "text-gray-400"
    }
  }

  return (
    <div
      className="bg-gray-900 border border-gray-800 rounded-lg p-4 hover:border-gray-700 transition-colors cursor-pointer"
      onClick={() => onSelect?.(contact)}
    >
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-bold text-lg">{contact.name}</h3>
        <span className={`text-xs font-medium uppercase ${getRoleColor(contact.role)}`}>
          {contact.role}
        </span>
      </div>
      <div className="space-y-1 text-sm">
        <div className="text-gray-400">
          <span className="text-gray-500">Wallet:</span>
          <span className="font-mono ml-2">{contact.walletAddress}</span>
        </div>
        {contact.reputationScore !== undefined && (
          <div className="text-gray-400">
            <span className="text-gray-500">Reputation:</span>
            <span className="ml-2">{contact.reputationScore}/100</span>
          </div>
        )}
        {contact.notes && (
          <div className="text-gray-500 text-xs mt-2">{contact.notes}</div>
        )}
      </div>
    </div>
  )
}
