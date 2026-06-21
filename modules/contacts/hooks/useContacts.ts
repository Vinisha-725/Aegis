// Custom hook for contacts management
// This will integrate with real API later

import { useState, useEffect } from "react"
import * as contactsApi from "../services/contacts.api"
import type { Contact, ContactFormData } from "../types/contact.types"

export function useContacts() {
  const [contacts, setContacts] = useState<Contact[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchContacts = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await contactsApi.getAllContacts()
      setContacts(data)
    } catch (err) {
      setError("Failed to fetch contacts")
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const createContact = async (data: ContactFormData) => {
    setLoading(true)
    setError(null)
    try {
      const newContact = await contactsApi.createContact(data)
      setContacts((prev) => [...prev, newContact])
      return newContact
    } catch (err) {
      setError("Failed to create contact")
      console.error(err)
      return null
    } finally {
      setLoading(false)
    }
  }

  const updateContact = async (id: string, data: Partial<ContactFormData>) => {
    setLoading(true)
    setError(null)
    try {
      const updatedContact = await contactsApi.updateContact(id, data)
      if (updatedContact) {
        setContacts((prev) => prev.map((c) => (c.id === id ? updatedContact : c)))
      }
      return updatedContact
    } catch (err) {
      setError("Failed to update contact")
      console.error(err)
      return null
    } finally {
      setLoading(false)
    }
  }

  const deleteContact = async (id: string) => {
    setLoading(true)
    setError(null)
    try {
      const success = await contactsApi.deleteContact(id)
      if (success) {
        setContacts((prev) => prev.filter((c) => c.id !== id))
      }
      return success
    } catch (err) {
      setError("Failed to delete contact")
      console.error(err)
      return false
    } finally {
      setLoading(false)
    }
  }

  const getContactsByRole = async (role: "client" | "freelancer") => {
    setLoading(true)
    setError(null)
    try {
      const data = await contactsApi.getContactsByRole(role)
      return data
    } catch (err) {
      setError("Failed to fetch contacts by role")
      console.error(err)
      return []
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchContacts()
  }, [])

  return {
    contacts,
    loading,
    error,
    createContact,
    updateContact,
    deleteContact,
    getContactsByRole,
    refetch: fetchContacts,
  }
}
