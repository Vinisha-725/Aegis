use anchor_lang::prelude::*;
use crate::state::*;
use crate::errors::*;

#[derive(Accounts)]
pub struct ReleasePayment<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(mut)]
    pub escrow: Account<'info, Escrow>,
}

pub fn handler(
    ctx: Context<ReleasePayment>,
) -> Result<()> {
    let escrow = &mut ctx.accounts.escrow;

    if escrow.status != EscrowStatus::Locked {
        return err!(AegisError::InvalidEscrowState);
    }

    escrow.status = EscrowStatus::Released;

    Ok(())
}
