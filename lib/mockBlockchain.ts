// Mock blockchain service layer for Aegis Protocol
// This will be replaced with real Solana program calls later
// Aligned with Anchor contract structure in programs/aegis_protocol/src/

export type EscrowStatus = "Locked" | "Released" | "Refunded" | "Disputed"

export interface Escrow {
  id: string
  client: string // Pubkey
  freelancer: string // Pubkey
  mint: string // Pubkey - USDC mint address
  amount: number // u64
  milestoneId: number // u64
  status: EscrowStatus
  bump?: number // u8 - PDA bump
  txHash?: string
  
  // Phase 3: Vault PDA (placeholder)
  vault?: string
  
  // Phase 4: Token account addresses (placeholder)
  clientTokenAccount?: string
  freelancerTokenAccount?: string
  vaultTokenAccount?: string
}

// In-memory storage for demo purposes
let escrows: Map<string, Escrow> = new Map()

// Helper to generate fake Solana-style transaction hash
function generateTxHash(): string {
  const chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
  let hash = ""
  for (let i = 0; i < 44; i++) {
    hash += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return hash
}

// Helper to generate fake escrow ID
function generateEscrowId(): string {
  return `escrow_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

// Simulate blockchain delay
function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export async function createEscrow(
  client: string,
  freelancer: string,
  mint: string,
  amount: number,
  milestoneId: number
): Promise<{ escrowId: string; txHash: string }> {
  await delay(1000) // Simulate blockchain transaction delay

  const escrowId = generateEscrowId()
  const txHash = generateTxHash()
  const bump = Math.floor(Math.random() * 255) // Mock PDA bump

  const escrow: Escrow = {
    id: escrowId,
    client,
    freelancer,
    mint,
    amount,
    milestoneId,
    status: "Locked",
    bump,
    txHash,
  }

  escrows.set(escrowId, escrow)

  console.log(`[MockBlockchain] Created escrow:`, escrow)
  console.log(`[MockBlockchain] Transaction hash: ${txHash}`)

  return { escrowId, txHash }
}

export async function releasePayment(escrowId: string): Promise<{ txHash: string }> {
  await delay(1500) // Simulate blockchain transaction delay

  const escrow = escrows.get(escrowId)
  if (!escrow) {
    throw new Error(`Escrow ${escrowId} not found`)
  }

  if (escrow.status !== "Locked") {
    throw new Error(`Escrow ${escrowId} is not in Locked state`)
  }

  escrow.status = "Released"
  escrow.txHash = generateTxHash()

  console.log(`[MockBlockchain] Released payment for escrow:`, escrowId)
  console.log(`[MockBlockchain] Transaction hash: ${escrow.txHash}`)

  return { txHash: escrow.txHash }
}

export async function refundEscrow(escrowId: string): Promise<{ txHash: string }> {
  await delay(1500) // Simulate blockchain transaction delay

  const escrow = escrows.get(escrowId)
  if (!escrow) {
    throw new Error(`Escrow ${escrowId} not found`)
  }

  if (escrow.status !== "Locked") {
    throw new Error(`Escrow ${escrowId} is not in Locked state`)
  }

  escrow.status = "Refunded" // Changed from "Disputed" to match contract
  escrow.txHash = generateTxHash()

  console.log(`[MockBlockchain] Refunded escrow:`, escrowId)
  console.log(`[MockBlockchain] Transaction hash: ${escrow.txHash}`)

  return { txHash: escrow.txHash }
}

export async function getEscrow(escrowId: string): Promise<Escrow | null> {
  await delay(500) // Simulate network delay

  const escrow = escrows.get(escrowId)
  if (!escrow) {
    return null
  }

  console.log(`[MockBlockchain] Retrieved escrow:`, escrowId)
  return { ...escrow }
}

export async function simulateAI(escrowId: string, approved: boolean): Promise<{ status: EscrowStatus }> {
  await delay(800) // Simulate AI processing delay

  const escrow = escrows.get(escrowId)
  if (!escrow) {
    throw new Error(`Escrow ${escrowId} not found`)
  }

  // AI simulation doesn't change the actual blockchain state
  // It just provides a recommendation
  console.log(`[MockBlockchain] AI ${approved ? "approved" : "rejected"} escrow:`, escrowId)

  return { status: escrow.status }
}

export async function getAllEscrows(): Promise<Escrow[]> {
  await delay(300)
  return Array.from(escrows.values())
}

// Reset function for testing
export function resetMockData(): void {
  escrows.clear()
  console.log("[MockBlockchain] Mock data reset")
}

// ============================================================================
// PHASE 3: Vault PDA (Placeholder)
// ============================================================================

export async function createVault(escrowId: string): Promise<{ vaultAddress: string; txHash: string }> {
  await delay(1000)
  
  const escrow = escrows.get(escrowId)
  if (!escrow) {
    throw new Error(`Escrow ${escrowId} not found`)
  }

  const vaultAddress = `vault_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  escrow.vault = vaultAddress
  escrow.txHash = generateTxHash()

  console.log(`[MockBlockchain] Created vault for escrow:`, escrowId)
  console.log(`[MockBlockchain] Vault address: ${vaultAddress}`)

  return { vaultAddress, txHash: escrow.txHash }
}

// ============================================================================
// PHASE 4: SPL Token Transfer (Placeholder)
// ============================================================================

export async function depositTokens(
  escrowId: string,
  amount: number
): Promise<{ txHash: string }> {
  await delay(1500)

  const escrow = escrows.get(escrowId)
  if (!escrow) {
    throw new Error(`Escrow ${escrowId} not found`)
  }

  // Mock token account addresses
  escrow.clientTokenAccount = `client_ta_${Math.random().toString(36).substr(2, 8)}`
  escrow.vaultTokenAccount = `vault_ta_${Math.random().toString(36).substr(2, 8)}`
  escrow.txHash = generateTxHash()

  console.log(`[MockBlockchain] Deposited ${amount} tokens to vault for escrow:`, escrowId)

  return { txHash: escrow.txHash }
}

export async function transferToFreelancer(escrowId: string): Promise<{ txHash: string }> {
  await delay(1500)

  const escrow = escrows.get(escrowId)
  if (!escrow) {
    throw new Error(`Escrow ${escrowId} not found`)
  }

  escrow.freelancerTokenAccount = `freelancer_ta_${Math.random().toString(36).substr(2, 8)}`
  escrow.txHash = generateTxHash()

  console.log(`[MockBlockchain] Transferred tokens to freelancer for escrow:`, escrowId)

  return { txHash: escrow.txHash }
}

export async function refundToClient(escrowId: string): Promise<{ txHash: string }> {
  await delay(1500)

  const escrow = escrows.get(escrowId)
  if (!escrow) {
    throw new Error(`Escrow ${escrowId} not found`)
  }

  escrow.txHash = generateTxHash()

  console.log(`[MockBlockchain] Refunded tokens to client for escrow:`, escrowId)

  return { txHash: escrow.txHash }
}

// ============================================================================
// PHASE 5: AI Approval Connection (Placeholder)
// ============================================================================

export async function aiApproveMilestone(escrowId: string): Promise<{ approved: boolean; confidence: number }> {
  await delay(2000) // Simulate AI processing

  const escrow = escrows.get(escrowId)
  if (!escrow) {
    throw new Error(`Escrow ${escrowId} not found`)
  }

  // Mock AI decision
  const approved = Math.random() > 0.3 // 70% chance of approval
  const confidence = 0.7 + Math.random() * 0.3 // 70-100% confidence

  console.log(`[MockBlockchain] AI ${approved ? "approved" : "rejected"} milestone for escrow:`, escrowId)
  console.log(`[MockBlockchain] AI confidence: ${(confidence * 100).toFixed(1)}%`)

  return { approved, confidence }
}

// ============================================================================
// PHASE 6: Reputation System (Placeholder)
// ============================================================================

export interface ReputationScore {
  freelancer: string
  score: number
  completedEscrows: number
  totalEscrows: number
}

export async function getReputation(freelancerAddress: string): Promise<ReputationScore> {
  await delay(500)

  // Mock reputation data
  const score = Math.floor(60 + Math.random() * 40) // 60-100 score
  const completedEscrows = Math.floor(Math.random() * 20)
  const totalEscrows = completedEscrows + Math.floor(Math.random() * 5)

  console.log(`[MockBlockchain] Retrieved reputation for freelancer:`, freelancerAddress)

  return {
    freelancer: freelancerAddress,
    score,
    completedEscrows,
    totalEscrows,
  }
}

export async function updateReputation(
  freelancerAddress: string,
  outcome: "success" | "failure"
): Promise<{ newScore: number }> {
  await delay(500)

  const current = await getReputation(freelancerAddress)
  const scoreChange = outcome === "success" ? 5 : -10
  const newScore = Math.min(100, Math.max(0, current.score + scoreChange))

  console.log(`[MockBlockchain] Updated reputation for freelancer:`, freelancerAddress)
  console.log(`[MockBlockchain] Score change: ${scoreChange > 0 ? "+" : ""}${scoreChange}`)

  return { newScore }
}

