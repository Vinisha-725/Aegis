# Aegis Protocol - Blockchain Setup Guide

Run these commands in WSL2 (Ubuntu) to set up and deploy the Solana program.

## Step 1: Access WSL2

```bash
# Open WSL2 from Windows PowerShell or Command Prompt
wsl
```

## Step 2: Update System and Install Dependencies

```bash
# Update package list
sudo apt update

# Install required packages
sudo apt install -y build-essential pkg-config libssl-dev curl git
```

## Step 3: Install Rust

```bash
# Install Rust using rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Source Rust environment
source $HOME/.cargo/env

# Verify installation
rustc --version
cargo --version
```

## Step 4: Install Solana CLI

```bash
# Install Solana CLI
sh -c "$(curl -sSfL https://release.solana.com/v1.18.4/install)"

# Add Solana to PATH
export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"

# Verify installation
solana --version
```

## Step 5: Install Anchor

```bash
# Install Anchor using cargo
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force

# Install Anchor CLI
avm install latest
avm use latest

# Verify installation
anchor --version
```

## Step 6: Configure Solana for Localnet

```bash
# Set Solana config to localnet
solana config set --url localhost

# Generate a new keypair if needed
solana-keygen new

# Check your address
solana address
```

## Step 7: Start Solana Test Validator

```bash
# Start the local validator (run in a separate terminal)
solana-test-validator
```

## Step 8: Navigate to Project Directory

```bash
# Navigate to the Aegis project directory (adjust path as needed)
cd /mnt/d/project/Aegis
```

## Step 9: Build the Anchor Program

```bash
# Build the program
anchor build
```

## Step 10: Get Program ID

```bash
# After build, get the program ID
anchor keys list
```

## Step 11: Update Program ID in Code

Replace `YOUR_PROGRAM_ID` in these files with the actual program ID from Step 10:

1. `programs/aegis_protocol/src/lib.rs` - Line: `declare_id!("YOUR_PROGRAM_ID");`
2. `Anchor.toml` - Lines: `[programs.localnet]`, `[programs.devnet]`, `[programs.mainnet]`

## Step 12: Deploy the Program

```bash
# Deploy to localnet (ensure solana-test-validator is running)
anchor deploy
```

## Step 13: Verify Deployment

```bash
# Check if program is deployed
solana program show <PROGRAM_ID>
```

## Step 14: Run Tests (Optional)

```bash
# Create a test file first (tests/aegis_protocol.ts)
# Then run tests
anchor test
```

## Troubleshooting

**If Solana CLI is not found after installation:**
```bash
# Add to .bashrc for persistence
echo 'export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**If Anchor is not found:**
```bash
# Add to .bashrc
echo 'export PATH="$HOME/.avm/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**If build fails:**
```bash
# Clean and rebuild
anchor clean
anchor build
```

## Next Steps

After deployment, you can:
1. Update the frontend mock to use the real program ID
2. Create TypeScript tests to interact with the deployed program
3. Integrate the frontend with the actual Solana program using @solana/web3.js
