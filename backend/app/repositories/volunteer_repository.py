
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.claim import Claim, ClaimStatus

class VolunteerRepository:
    """
    Handles database operations for volunteers managing claims.
    """
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_claim_by_id(
        self, 
        volunteer_id: int,
        donation_id: int
    ) -> Claim | None:
        """
        Retrieves a claim by its ID for a specific volunteer.
        """
        result = await self.db.execute(
            select(Claim).where(
                Claim.volunteer_id == volunteer_id,
                Claim.donation_id == donation_id
            )
        )
        return result.scalar_one_or_none()


    async def update_claim_status(
        self, 
        claim: Claim, 
        new_status: ClaimStatus
    ) -> Claim:
        """
        Updates the status of an existing claim.
        """
        claim.status = new_status
        await self.db.commit()
        await self.db.refresh(claim)
        return claim


    async def update_proof_image_url(self, claim: Claim, proof_image_url: str) -> Claim:
        """
        Updates the proof image URL of an existing claim.
        """
        claim.image_proof_url = proof_image_url
        await self.db.commit()
        await self.db.refresh(claim)
        return claim


    async def create_claim(
        self, 
        donation_id: int, 
        volunteer_id: int
    ) -> Claim:
        """
        Creates a new claim for a donation by a volunteer.
        """
        new_claim = Claim(
            donation_id=donation_id,
            volunteer_id=volunteer_id,
            status=ClaimStatus.PENDING
        )
        self.db.add(new_claim)
        await self.db.commit()
        await self.db.refresh(new_claim)
        return new_claim

