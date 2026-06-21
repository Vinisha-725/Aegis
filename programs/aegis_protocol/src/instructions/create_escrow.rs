use anchor_lang::prelude::*;
use crate::state::*;

#[derive(Accounts)]
#[instruction(amount: u64, milestone_id: u64)]
pub struct CreateEscrow<'info> {
    #[account(mut)]
    pub client: Signer<'info>,

    /// CHECK:
    pub freelancer: UncheckedAccount<'info>,

    pub mint: Account<'info, anchor_spl::token::Mint>,

    #[account(
        init,
        payer = client,
        space = 8 + Escrow::LEN,
        seeds = [
            b"escrow",
            client.key().as_ref(),
            &milestone_id.to_le_bytes()
        ],
        bump
    )]
    pub escrow: Account<'info, Escrow>,

    pub system_program: Program<'info, System>,
}

pub fn handler(
    ctx: Context<CreateEscrow>,
    amount: u64,
    milestone_id: u64,
) -> Result<()> {
    let escrow = &mut ctx.accounts.escrow;

    escrow.client = ctx.accounts.client.key();
    escrow.freelancer = ctx.accounts.freelancer.key();
    escrow.mint = ctx.accounts.mint.key();
    escrow.amount = amount;
    escrow.milestone_id = milestone_id;
    escrow.status = EscrowStatus::Locked;
    escrow.bump = ctx.bumps.escrow;

    Ok(())
}
