// Contact list component for displaying all contacts

import type { Contact } from "../types/contact.types"
import { ContactCard } from "./ContactCard"

interface ContactListProps {
  contacts: Contact[]
  onSelectContact?: (contact: Contact) => void
  emptyMessage?: string
}

export function ContactList({ contacts, onSelectContact, emptyMessage = "No contacts found" }: ContactListProps) {
  if (contacts.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8">
        {emptyMessage}
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {contacts.map((contact) => (
        <ContactCard
          key={contact.id}
          contact={contact}
          onSelect={onSelectContact}
        />
      ))}
    </div>
  )
}
