// Mock API layer for contacts
// This will be replaced with real backend calls later

import type { Contact, ContactFormData } from "../types/contact.types"

// In-memory storage for demo purposes
let contacts: Map<string, Contact> = new Map()

// Helper to generate fake contact ID
function generateContactId(): string {
  return `contact_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

// Simulate network delay
function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export async function createContact(data: ContactFormData): Promise<Contact> {
  await delay(500)

  const id = generateContactId()
  const contact: Contact = {
    id,
    ...data,
    createdAt: new Date().toISOString(),
  }

  contacts.set(id, contact)

  console.log(`[ContactsAPI] Created contact:`, contact)
  return contact
}

export async function getContact(id: string): Promise<Contact | null> {
  await delay(300)
  const contact = contacts.get(id)
  return contact ? { ...contact } : null
}

export async function getAllContacts(): Promise<Contact[]> {
  await delay(300)
  return Array.from(contacts.values())
}

export async function getContactsByRole(role: "client" | "freelancer"): Promise<Contact[]> {
  await delay(300)
  return Array.from(contacts.values()).filter((c) => c.role === role)
}

export async function updateContact(id: string, data: Partial<ContactFormData>): Promise<Contact | null> {
  await delay(500)

  const contact = contacts.get(id)
  if (!contact) {
    return null
  }

  const updatedContact = { ...contact, ...data }
  contacts.set(id, updatedContact)

  console.log(`[ContactsAPI] Updated contact:`, id)
  return updatedContact
}

export async function deleteContact(id: string): Promise<boolean> {
  await delay(500)

  const result = contacts.delete(id)
  console.log(`[ContactsAPI] Deleted contact:`, id)
  return result
}

// Reset function for testing
export function resetContactsData(): void {
  contacts.clear()
  console.log("[ContactsAPI] Contacts data reset")
}
