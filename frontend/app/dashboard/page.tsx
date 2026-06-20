"use client"

import { useState } from "react"
import Link from "next/link"
import {
  createEscrow,
  releasePayment,
  refundEscrow,
  getEscrow,
  simulateAI,
  type Escrow,
  type EscrowStatus,
} from "@/lib/mockBlockchain"

export default function Dashboard() {
  const [client, setClient] = useState("")
  const [freelancer, setFreelancer] = useState("")
  const [mint, setMint] = useState("")
  const [amount, setAmount] = useState("")
  const [milestoneId, setMilestoneId] = useState("")
  const [currentEscrow, setCurrentEscrow] = useState<Escrow | null>(null)
  const [loading, setLoading] = useState(false)
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" } | null>(null)

  const showToast = (message: string, type: "success" | "error") => {
    setToast({ message, type })
    setTimeout(() => setToast(null), 3000)
  }

  const handleCreateEscrow = async () => {
    if (!client || !freelancer || !mint || !amount || !milestoneId) {
      showToast("Please fill all fields", "error")
      return
    }

    setLoading(true)
    try {
      const result = await createEscrow(client, freelancer, mint, Number(amount), Number(milestoneId))
      const escrow = await getEscrow(result.escrowId)
      if (escrow) {
        setCurrentEscrow(escrow)
      }
      showToast(`Escrow created! ID: ${result.escrowId}`, "success")
      // Clear form
      setClient("")
      setFreelancer("")
      setMint("")
      setAmount("")
      setMilestoneId("")
    } catch (error) {
      showToast("Failed to create escrow", "error")
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleReleasePayment = async () => {
    if (!currentEscrow) return

    setLoading(true)
    try {
      const result = await releasePayment(currentEscrow.id)
      const updatedEscrow = await getEscrow(currentEscrow.id)
      if (updatedEscrow) {
        setCurrentEscrow(updatedEscrow)
      }
      showToast(`Payment released! TX: ${result.txHash}`, "success")
    } catch (error) {
      showToast("Failed to release payment", "error")
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleRefundEscrow = async () => {
    if (!currentEscrow) return

    setLoading(true)
    try {
      const result = await refundEscrow(currentEscrow.id)
      const updatedEscrow = await getEscrow(currentEscrow.id)
      if (updatedEscrow) {
        setCurrentEscrow(updatedEscrow)
      }
      showToast(`Escrow refunded! TX: ${result.txHash}`, "success")
    } catch (error) {
      showToast("Failed to refund escrow", "error")
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleSimulateAIApproval = async () => {
    if (!currentEscrow) return

    setLoading(true)
    try {
      await simulateAI(currentEscrow.id, true)
      showToast("AI approved the milestone", "success")
    } catch (error) {
      showToast("AI simulation failed", "error")
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleSimulateAIRejection = async () => {
    if (!currentEscrow) return

    setLoading(true)
    try {
      await simulateAI(currentEscrow.id, false)
      showToast("AI rejected the milestone", "success")
    } catch (error) {
      showToast("AI simulation failed", "error")
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: EscrowStatus) => {
    switch (status) {
      case "Locked":
        return "text-yellow-400"
      case "Released":
        return "text-green-400"
      case "Refunded":
        return "text-orange-400"
      case "Disputed":
        return "text-red-400"
    }
  }

  return (
    <div className="min-h-screen bg-black text-gray-100 p-8">
      {/* Header */}
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-green-400">Aegis Protocol</h1>
          <p className="text-gray-400">Blockchain Test Console</p>
        </div>
        <Link href="/">
          <button className="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors">
            Back to Home
          </button>
        </Link>
      </div>

      {/* Toast Notification */}
      {toast && (
        <div
          className={`fixed top-4 right-4 px-6 py-3 rounded-lg ${
            toast.type === "success" ? "bg-green-600" : "bg-red-600"
          } text-white font-medium z-50`}
        >
          {toast.message}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Section A: Create Escrow */}
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4 text-green-400">Create Escrow</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Client Wallet Address</label>
              <input
                type="text"
                value={client}
                onChange={(e) => setClient(e.target.value)}
                placeholder="Enter client wallet address"
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Freelancer Wallet Address</label>
              <input
                type="text"
                value={freelancer}
                onChange={(e) => setFreelancer(e.target.value)}
                placeholder="Enter freelancer wallet address"
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Mint Address (USDC)</label>
              <input
                type="text"
                value={mint}
                onChange={(e) => setMint(e.target.value)}
                placeholder="Enter mint address"
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Amount (USDC)</label>
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="Enter amount"
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Milestone ID</label>
              <input
                type="number"
                value={milestoneId}
                onChange={(e) => setMilestoneId(e.target.value)}
                placeholder="Enter milestone ID"
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-green-500"
              />
            </div>
            <button
              onClick={handleCreateEscrow}
              disabled={loading}
              className="w-full px-4 py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-lg font-bold transition-colors"
            >
              {loading ? "Processing..." : "Create Escrow"}
            </button>
          </div>
        </div>

        {/* Section B: Escrow Viewer */}
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4 text-green-400">Escrow Viewer</h2>
          {currentEscrow ? (
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-400">Escrow ID:</span>
                <span className="font-mono text-sm">{currentEscrow.id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Status:</span>
                <span className={`font-bold ${getStatusColor(currentEscrow.status)}`}>
                  {currentEscrow.status}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Amount:</span>
                <span className="font-bold">{currentEscrow.amount} USDC</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Milestone ID:</span>
                <span className="font-mono text-sm">{currentEscrow.milestoneId}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Mint:</span>
                <span className="font-mono text-xs">{currentEscrow.mint}</span>
              </div>
              {currentEscrow.bump !== undefined && (
                <div className="flex justify-between">
                  <span className="text-gray-400">PDA Bump:</span>
                  <span className="font-mono text-sm">{currentEscrow.bump}</span>
                </div>
              )}
              <div className="border-t border-gray-700 pt-3 mt-3">
                <div className="text-sm text-gray-400 mb-2">Parties:</div>
                <div className="space-y-2">
                  <div className="bg-gray-800 p-2 rounded">
                    <div className="text-xs text-gray-500">Client</div>
                    <div className="font-mono text-xs">{currentEscrow.client}</div>
                  </div>
                  <div className="bg-gray-800 p-2 rounded">
                    <div className="text-xs text-gray-500">Freelancer</div>
                    <div className="font-mono text-xs">{currentEscrow.freelancer}</div>
                  </div>
                </div>
              </div>
              {currentEscrow.txHash && (
                <div className="border-t border-gray-700 pt-3 mt-3">
                  <div className="text-sm text-gray-400">Transaction Hash:</div>
                  <div className="font-mono text-xs text-green-400">{currentEscrow.txHash}</div>
                </div>
              )}
            </div>
          ) : (
            <p className="text-gray-500">No escrow selected. Create an escrow to view details.</p>
          )}
        </div>

        {/* Section C: AI Simulation Panel */}
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4 text-green-400">AI Simulation Panel</h2>
          <div className="space-y-3">
            <p className="text-sm text-gray-400">
              Simulate AI approval/rejection for milestone completion
            </p>
            <div className="flex gap-3">
              <button
                onClick={handleSimulateAIApproval}
                disabled={loading || !currentEscrow}
                className="flex-1 px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-lg font-bold transition-colors"
              >
                {loading ? "Processing..." : "Simulate AI Approval"}
              </button>
              <button
                onClick={handleSimulateAIRejection}
                disabled={loading || !currentEscrow}
                className="flex-1 px-4 py-3 bg-orange-600 hover:bg-orange-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-lg font-bold transition-colors"
              >
                {loading ? "Processing..." : "Simulate AI Rejection"}
              </button>
            </div>
          </div>
        </div>

        {/* Section D: Blockchain Actions */}
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4 text-green-400">Blockchain Actions</h2>
          <div className="space-y-3">
            <p className="text-sm text-gray-400">
              Execute blockchain transactions on the escrow
            </p>
            <div className="flex gap-3">
              <button
                onClick={handleReleasePayment}
                disabled={loading || !currentEscrow || currentEscrow.status !== "Locked"}
                className="flex-1 px-4 py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-lg font-bold transition-colors"
              >
                {loading ? "Processing..." : "Release Payment"}
              </button>
              <button
                onClick={handleRefundEscrow}
                disabled={loading || !currentEscrow || currentEscrow.status !== "Locked"}
                className="flex-1 px-4 py-3 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-lg font-bold transition-colors"
              >
                {loading ? "Processing..." : "Refund Escrow"}
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2">
              Note: Actions are only available when escrow is in "Locked" status
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
