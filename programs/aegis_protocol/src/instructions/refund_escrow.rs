use anchor_lang::prelude::*;
use crate::state::*;
use crate::errors::*;

#[derive(Accounts)]
pub struct RefundEscrow<'info> {
    #[account(mut)]
    pub client: Signer<'info>,

    #[account(mut)]
    pub escrow: Account<'info, Escrow>,
}

pub fn handler(
    ctx: Context<RefundEscrow>,
) -> Result<()> {
    let escrow = &mut ctx.accounts.escrow;

    if escrow.client != ctx.accounts.client.key() {
        return err!(AegisError::Unauthorized);
    }

    if escrow.status != EscrowStatus::Locked {
        return err!(AegisError::InvalidEscrowState);
    }

    escrow.status = EscrowStatus::Refunded;

    Ok(())
}
