# claim_service.py — Business logic for claiming, status transitions, handoff confirmation


from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile


from app.repositories.volunteer_repository import VolunteerRepository
from app.repositories.photo_repository import PhotoRepository
from app.repositories.user_repository import UserRepository
from app.models.claim import Claim, ClaimStatus
from app.models.photo import PhotoPurpose
from app.exceptions import AlreadyExistsError, PermissionDeniedError, NotFoundError
from app.utils.image_helper import save_image


class ClaimService:
    def __init__(
        self, 
        db: AsyncSession, 
        repo: VolunteerRepository,
        photo_repo: PhotoRepository,
        user_repo: UserRepository,
    ):
        self.db = db
        self.repo = repo
        self.photo_repo = photo_repo
        self.user_repo = user_repo


    async def check_claim_exist(
        self,
        volunteer_id: int,
        donation_id: int
    ) -> Claim:
        """
        Checks if a claim already exists for a given volunteer.
        """
        claim = await self.repo.get_claim_by_id(volunteer_id, donation_id)
        if claim:
            raise AlreadyExistsError("Claim already exists for this volunteer.")
        return claim


    async def request_claim(
        self,
        volunteer_id: int,
        donation_id: int
    ) -> Claim:
        """
        Creates a new claim for a donation by a volunteer.
        """
        await self.check_claim_exist(volunteer_id, donation_id)
        result = await self.repo.create_claim(donation_id, volunteer_id)
        return result


    async def update_claim_status(
        self,
        volunteer_id: int,
        donation_id: int,
        new_status: ClaimStatus,
        proof_image: UploadFile | None = None
    ) -> Claim:
        """"
        Updates the status of an existing claim for a volunteer.
        """
        role = await self.user_repo.get_user_role(volunteer_id)
        if role != "volunteer":
            raise PermissionDeniedError("Only volunteers can update claim status.")

        claim = await self.repo.get_claim_by_id(volunteer_id, donation_id)
        if not claim:
            raise NotFoundError("Claim not found.")
        if proof_image is not None and new_status != ClaimStatus.COMPLETED:
            raise PermissionDeniedError(
                "A proof image can only be submitted for a completed claim."
            )

        updated_claim = await self.repo.update_claim_status(claim, new_status)

        if proof_image is not None:
            proof_image_url = await save_image(
                PhotoPurpose.DELIVERY_PROOF,
                proof_image,
            )
            await self.photo_repo.create_photo(
                volunteer_id,
                proof_image_url,
                PhotoPurpose.DELIVERY_PROOF,
            )
            updated_claim = await self.repo.update_proof_image_url(
                updated_claim,
                proof_image_url,
            )
        return updated_claim
