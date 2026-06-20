use anchor_lang::prelude::*;

pub mod state;
pub mod instructions;
pub mod errors;

use instructions::*;

declare_id!("YOUR_PROGRAM_ID");

#[program]
pub mod aegis_protocol {
    use super::*;

    pub fn create_escrow(
        ctx: Context<CreateEscrow>,
        amount: u64,
        milestone_id: u64,
    ) -> Result<()> {
        create_escrow::handler(ctx, amount, milestone_id)
    }

    pub fn release_payment(
        ctx: Context<ReleasePayment>,
    ) -> Result<()> {
        release_payment::handler(ctx)
    }

    pub fn refund_escrow(
        ctx: Context<RefundEscrow>,
    ) -> Result<()> {
        refund_escrow::handler(ctx)
    }
}
