use anchor_lang::prelude::*;

#[error_code]
pub enum AegisError {
    #[msg("Escrow is not locked.")]
    InvalidEscrowState,

    #[msg("Unauthorized.")]
    Unauthorized,
}
