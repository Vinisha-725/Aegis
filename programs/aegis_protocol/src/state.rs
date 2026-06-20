use anchor_lang::prelude::*;

#[account]
pub struct Escrow {
    pub client: Pubkey,
    pub freelancer: Pubkey,
    pub mint: Pubkey,

    pub amount: u64,

    pub milestone_id: u64,

    pub status: EscrowStatus,

    pub bump: u8,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, PartialEq, Eq)]
pub enum EscrowStatus {
    Locked,
    Released,
    Refunded,
    Disputed,
}

impl Escrow {
    pub const LEN: usize =
        32 + // client
        32 + // freelancer
        32 + // mint
        8 +  // amount
        8 +  // milestone
        1 +  // enum
        1;   // bump
}
