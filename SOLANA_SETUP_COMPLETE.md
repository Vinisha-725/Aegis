# Solana Blockchain Setup - Complete Guide

Run these commands in WSL2 to set up Solana, deploy the program, and integrate with the frontend.

## Step 1: Open WSL2

```bash
# From Windows PowerShell or Command Prompt
wsl
```

## Step 2: Install Dependencies

```bash
# Update package list
sudo apt update

# Install required packages
sudo apt install -y build-essential pkg-config libssl-dev curl git
```

## Step 3: Install Rust

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Source Rust environment
source $HOME/.cargo/env

# Verify
rustc --version
cargo --version
```

## Step 4: Install Solana CLI

```bash
# Install Solana CLI
sh -c "$(curl -sSfL https://release.solana.com/v1.18.4/install)"

# Add to PATH
export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"

# Add to .bashrc for persistence
echo 'export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify
solana --version
```

## Step 5: Install Anchor

```bash
# Install Anchor Version Manager
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force

# Install latest Anchor
avm install latest
avm use latest

# Add to PATH
echo 'export PATH="$HOME/.avm/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify
anchor --version
```

## Step 6: Configure Solana

```bash
# Set to localnet
solana config set --url localhost

# Generate new keypair
solana-keygen new --no-bip39-passphrase

# Check address
solana address
```

## Step 7: Start Solana Test Validator

```bash
# Run this in a separate WSL2 terminal and keep it running
solana-test-validator
```

## Step 8: Navigate to Project

```bash
# Navigate to the project (adjust path if needed)
cd /mnt/d/project/Aegis_github
```

## Step 9: Build the Program

```bash
# Build the Anchor program
anchor build
```

## Step 10: Get Program ID

```bash
# Get the program ID
anchor keys list
```

Copy the program ID (e.g., `8xQeWv...`) - you'll need this for the next step.

## Step 11: Update Program ID in Code

Replace `YOUR_PROGRAM_ID` in these files with the actual program ID:

**File: `programs/aegis_protocol/src/lib.rs`**
```rust
declare_id!("YOUR_PROGRAM_ID");  // Replace with actual ID
```

**File: `Anchor.toml`**
```toml
[programs.localnet]
aegis_protocol = "YOUR_PROGRAM_ID"  # Replace with actual ID
```

## Step 12: Rebuild with New Program ID

```bash
# Clean and rebuild
anchor clean
anchor build
```

## Step 13: Deploy the Program

```bash
# Deploy to localnet (ensure solana-test-validator is running)
anchor deploy
```

## Step 14: Verify Deployment

```bash
# Check if program is deployed
solana program show <PROGRAM_ID>
```

## Step 15: Update Frontend to Use Real Solana

Now update the frontend to connect to the real Solana program instead of the mock.

### Install Solana Web3.js Dependencies

```bash
# From Windows PowerShell (not WSL2)
cd d:\project\Aegis_github\frontend
npm install @solana/web3.js @solana/wallet-adapter-react @solana/wallet-adapter-react-ui @solana/wallet-adapter-wallets
```

### Create Real Blockchain Service

Create `frontend/lib/solanaBlockchain.ts`:

```typescript
import { 
  Connection, 
  PublicKey, 
  Keypair, 
  Transaction, 
  SystemProgram 
} from '@solana/web3.js';
import { 
  Program, 
  AnchorProvider, 
  web3 
} from '@project-serum/anchor';

// Replace with your actual program ID from Step 10
const PROGRAM_ID = new PublicKey('YOUR_PROGRAM_ID');

// Connection to localnet
const connection = new Connection('http://localhost:8899', 'confirmed');

// Get the IDL (Interface Definition Language)
// This will be generated after building the program
const idl = require('../target/idl/aegis_protocol.json');

export async function createEscrow(
  clientWallet: string,
  freelancerWallet: string,
  mint: string,
  amount: number,
  milestoneId: number
) {
  try {
    const provider = new AnchorProvider(
      connection,
      // Add wallet adapter here
      new Keypair(), // Placeholder - use actual wallet
      { commitment: 'confirmed' }
    );

    const program = new Program(idl, PROGRAM_ID, provider);

    const [escrowPda] = await web3.PublicKey.findProgramAddress(
      [
        Buffer.from('escrow'),
        new PublicKey(clientWallet).toBuffer(),
        Buffer.from(new Uint8Array([milestoneId]))
      ],
      PROGRAM_ID
    );

    const tx = await program.methods
      .createEscrow(new BN(amount), new BN(milestoneId))
      .accounts({
        client: new PublicKey(clientWallet),
        freelancer: new PublicKey(freelancerWallet),
        mint: new PublicKey(mint),
        escrow: escrowPda,
        systemProgram: SystemProgram.programId,
      })
      .rpc();

    return { escrowId: escrowPda.toString(), txHash: tx };
  } catch (error) {
    console.error('Error creating escrow:', error);
    throw error;
  }
}

export async function releasePayment(escrowId: string) {
  try {
    const provider = new AnchorProvider(
      connection,
      new Keypair(),
      { commitment: 'confirmed' }
    );

    const program = new Program(idl, PROGRAM_ID, provider);

    const tx = await program.methods
      .releasePayment()
      .accounts({
        authority: provider.wallet.publicKey,
        escrow: new PublicKey(escrowId),
      })
      .rpc();

    return { txHash: tx };
  } catch (error) {
    console.error('Error releasing payment:', error);
    throw error;
  }
}

export async function refundEscrow(escrowId: string) {
  try {
    const provider = new AnchorProvider(
      connection,
      new Keypair(),
      { commitment: 'confirmed' }
    );

    const program = new Program(idl, PROGRAM_ID, provider);

    const tx = await program.methods
      .refundEscrow()
      .accounts({
        client: provider.wallet.publicKey,
        escrow: new PublicKey(escrowId),
      })
      .rpc();

    return { txHash: tx };
  } catch (error) {
    console.error('Error refunding escrow:', error);
    throw error;
  }
}

export async function getEscrow(escrowId: string) {
  try {
    const escrowAccount = await connection.getAccountInfo(
      new PublicKey(escrowId)
    );

    if (!escrowAccount) {
      return null;
    }

    // Decode the account data using the IDL
    const program = new Program(idl, PROGRAM_ID, new AnchorProvider(connection, new Keypair(), {}));
    const escrowData = program.coder.accounts.decode('escrow', escrowAccount.data);

    return {
      id: escrowId,
      client: escrowData.client.toString(),
      freelancer: escrowData.freelancer.toString(),
      mint: escrowData.mint.toString(),
      amount: escrowData.amount.toNumber(),
      milestoneId: escrowData.milestoneId.toNumber(),
      status: escrowData.status,
      bump: escrowData.bump,
    };
  } catch (error) {
    console.error('Error getting escrow:', error);
    throw error;
  }
}
```

### Update Dashboard to Use Real Solana

In `frontend/app/dashboard/page.tsx`, replace the mock imports:

```typescript
// Replace this:
import {
  createEscrow,
  releasePayment,
  refundEscrow,
  getEscrow,
  simulateAI,
  type Escrow,
  type EscrowStatus,
} from "@/lib/mockBlockchain"

// With this:
import {
  createEscrow,
  releasePayment,
  refundEscrow,
  getEscrow,
} from "@/lib/solanaBlockchain"
import type { Escrow, EscrowStatus } from "@/lib/mockBlockchain"
```

## Step 16: Test the Integration

```bash
# From Windows PowerShell
cd d:\project\Aegis_github\frontend
npm run dev
```

Open http://localhost:3000 and test:
1. Create an escrow
2. Check the console for transaction logs
3. Verify the transaction on Solana explorer (localnet)

## Troubleshooting

**If solana-test-validator fails to start:**
```bash
# Kill any existing validator
pkill solana-test-validator

# Start fresh
solana-test-validator --reset
```

**If program deployment fails:**
```bash
# Check your balance
solana balance

# Airdrop SOL if needed
solana airdrop 2
```

**If frontend can't connect to localnet:**
- Ensure solana-test-validator is running
- Check that connection URL is `http://localhost:8899`
- Verify firewall isn't blocking port 8899

**If IDL file is missing:**
```bash
# The IDL is generated after build
# It should be at: target/idl/aegis_protocol.json
# If missing, run: anchor build
```

## Next Steps

After successful integration:
1. Add wallet connection (Phantom, Solflare, etc.)
2. Add actual SPL token transfers
3. Implement AI approval integration
4. Add reputation system
