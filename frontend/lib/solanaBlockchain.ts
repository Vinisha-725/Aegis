// Real Solana blockchain service for Aegis Protocol
// This connects to the actual deployed Solana program

import { 
  Connection, 
  PublicKey, 
  Keypair, 
  Transaction, 
  SystemProgram,
  BN
} from '@solana/web3.js';
import { 
  Program, 
  AnchorProvider, 
  web3,
  AnchorError
} from '@project-serum/anchor';

// TODO: Replace with your actual program ID after deployment
const PROGRAM_ID = new PublicKey('YOUR_PROGRAM_ID');

// Connection to localnet
const connection = new Connection('http://localhost:8899', 'confirmed');

// IDL will be loaded from target/idl/aegis_protocol.json after build
let idl: any = null;

// Load IDL dynamically
export async function loadIdl() {
  try {
    // Try to load from the build output
    const response = await fetch('/target/idl/aegis_protocol.json');
    idl = await response.json();
    return idl;
  } catch (error) {
    console.error('Failed to load IDL:', error);
    // Fallback to mock if IDL not available
    return null;
  }
}

// Get or create provider
export function getProvider(wallet?: any) {
  if (!wallet) {
    // Use a temporary keypair for testing (replace with actual wallet)
    const keypair = Keypair.generate();
    return new AnchorProvider(
      connection,
      keypair as any,
      { commitment: 'confirmed' }
    );
  }
  
  return new AnchorProvider(
    connection,
    wallet,
    { commitment: 'confirmed' }
  );
}

export async function createEscrow(
  clientWallet: string,
  freelancerWallet: string,
  mint: string,
  amount: number,
  milestoneId: number
): Promise<{ escrowId: string; txHash: string }> {
  try {
    if (!idl) {
      await loadIdl();
    }

    if (!idl) {
      throw new Error('IDL not loaded. Please build the Anchor program first.');
    }

    const provider = getProvider();
    const program = new Program(idl, PROGRAM_ID, provider);

    const clientPubkey = new PublicKey(clientWallet);
    const freelancerPubkey = new PublicKey(freelancerWallet);
    const mintPubkey = new PublicKey(mint);

    // Derive PDA for escrow account
    const [escrowPda] = await PublicKey.findProgramAddress(
      [
        Buffer.from('escrow'),
        clientPubkey.toBuffer(),
        Buffer.from(new Uint8Array([milestoneId]))
      ],
      PROGRAM_ID
    );

    const tx = await program.methods
      .createEscrow(new BN(amount), new BN(milestoneId))
      .accounts({
        client: clientPubkey,
        freelancer: freelancerPubkey,
        mint: mintPubkey,
        escrow: escrowPda,
        systemProgram: SystemProgram.programId,
      })
      .rpc();

    console.log(`[Solana] Created escrow: ${escrowPda.toString()}`);
    console.log(`[Solana] Transaction: ${tx}`);

    return { escrowId: escrowPda.toString(), txHash: tx };
  } catch (error) {
    console.error('[Solana] Error creating escrow:', error);
    
    // Handle Anchor errors
    if (error instanceof AnchorError) {
      console.error(`Error code: ${error.error.errorCode.number}`);
      console.error(`Error message: ${error.error.errorMessage}`);
    }
    
    throw error;
  }
}

export async function releasePayment(escrowId: string): Promise<{ txHash: string }> {
  try {
    if (!idl) {
      await loadIdl();
    }

    if (!idl) {
      throw new Error('IDL not loaded. Please build the Anchor program first.');
    }

    const provider = getProvider();
    const program = new Program(idl, PROGRAM_ID, provider);

    const escrowPubkey = new PublicKey(escrowId);

    const tx = await program.methods
      .releasePayment()
      .accounts({
        authority: provider.wallet.publicKey,
        escrow: escrowPubkey,
      })
      .rpc();

    console.log(`[Solana] Released payment for escrow: ${escrowId}`);
    console.log(`[Solana] Transaction: ${tx}`);

    return { txHash: tx };
  } catch (error) {
    console.error('[Solana] Error releasing payment:', error);
    
    if (error instanceof AnchorError) {
      console.error(`Error code: ${error.error.errorCode.number}`);
      console.error(`Error message: ${error.error.errorMessage}`);
    }
    
    throw error;
  }
}

export async function refundEscrow(escrowId: string): Promise<{ txHash: string }> {
  try {
    if (!idl) {
      await loadIdl();
    }

    if (!idl) {
      throw new Error('IDL not loaded. Please build the Anchor program first.');
    }

    const provider = getProvider();
    const program = new Program(idl, PROGRAM_ID, provider);

    const escrowPubkey = new PublicKey(escrowId);

    const tx = await program.methods
      .refundEscrow()
      .accounts({
        client: provider.wallet.publicKey,
        escrow: escrowPubkey,
      })
      .rpc();

    console.log(`[Solana] Refunded escrow: ${escrowId}`);
    console.log(`[Solana] Transaction: ${tx}`);

    return { txHash: tx };
  } catch (error) {
    console.error('[Solana] Error refunding escrow:', error);
    
    if (error instanceof AnchorError) {
      console.error(`Error code: ${error.error.errorCode.number}`);
      console.error(`Error message: ${error.error.errorMessage}`);
    }
    
    throw error;
  }
}

export async function getEscrow(escrowId: string) {
  try {
    if (!idl) {
      await loadIdl();
    }

    if (!idl) {
      throw new Error('IDL not loaded. Please build the Anchor program first.');
    }

    const escrowPubkey = new PublicKey(escrowId);
    const escrowAccount = await connection.getAccountInfo(escrowPubkey);

    if (!escrowAccount) {
      return null;
    }

    const program = new Program(idl, PROGRAM_ID, getProvider());
    const escrowData = program.coder.accounts.decode('escrow', escrowAccount.data);

    // Map status from enum to string
    const statusMap: { [key: number]: string } = {
      0: 'Locked',
      1: 'Released',
      2: 'Refunded',
      3: 'Disputed',
    };

    return {
      id: escrowId,
      client: escrowData.client.toString(),
      freelancer: escrowData.freelancer.toString(),
      mint: escrowData.mint.toString(),
      amount: escrowData.amount.toNumber(),
      milestoneId: escrowData.milestoneId.toNumber(),
      status: statusMap[escrowData.status] || 'Locked',
      bump: escrowData.bump,
    };
  } catch (error) {
    console.error('[Solana] Error getting escrow:', error);
    throw error;
  }
}

// Helper function to check if Solana is available
export async function checkSolanaConnection(): Promise<boolean> {
  try {
    await connection.getVersion();
    return true;
  } catch (error) {
    console.error('[Solana] Connection check failed:', error);
    return false;
  }
}

// Helper function to get account balance
export async function getBalance(pubkey: string): Promise<number> {
  try {
    const balance = await connection.getBalance(new PublicKey(pubkey));
    return balance / 1e9; // Convert lamports to SOL
  } catch (error) {
    console.error('[Solana] Error getting balance:', error);
    return 0;
  }
}
