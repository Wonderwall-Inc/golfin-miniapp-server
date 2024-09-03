import logging
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.social_media.models import SocialMediaModel
from app.social_media.schemas import (
    SocialMediaCategrizedBaseScehma,
    SocialMediaSchema,
    SocialMediaBaseSchema,
    SocialMediaCreateDetailScheam,
    SocialMediaCreateRequestSchema,
    SocialMediaCreateResponseSchema,
    SocialMediaRetrievalRequestSchema,
    SocialMediaRetrievalResponseSchema,
    SocialMediaUpdateRequestSchema,
    SocialMediaUpdateResponseSchema,
    YoutubeSocialMediaSchema,
    FacebookSocialMediaSchema,
    InstagramSocialMediaSchema,
    TelegramSocialMediaSchema,
    XSocialMediaSchema,
    DiscordSocialMedia,
    # TikTokSocialMediaSchema,
    # PinterestSocialMediaSchema,
    # RedditSocialMediaSchema,
    # DiscordSocialMediaSchema,
    # TwitchSocialMediaSchema,
    # PatreonSocialMediaSchema,
)


def create_social_media(
    request: SocialMediaCreateRequestSchema, db: Session
) -> SocialMediaCreateResponseSchema:
    if not request.user_id or not request.social_media or not request.type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID, type and social media are required",
        )

    social_media = (
        db.query(SocialMediaModel)
        .filter(SocialMediaModel.user_id == request.user_id)
        .first()
    )
    if social_media:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Social Media already exists",
        )
    if request.type == "youtube":
        new_social_media = SocialMediaModel(
            user_id=request.user_id,
            youtube_id=request.social_media.youtube.youtube_id,
            youtube_is_following=request.social_media.youtube.youtube_is_following,
            youtube_is_viewed=request.social_media.youtube.youtube_is_viewed,
            youtube_view_date=request.social_media.youtube.youtube_view_date,
            custom_logs=request.social_media.custom_logs,
        )
        db.add(new_social_media)
        db.commit()
        db.refresh(new_social_media)
        return SocialMediaCreateResponseSchema(
            user_id=new_social_media.user_id,
            social_media=SocialMediaBaseSchema(
                id=new_social_media.id,
                youtube=YoutubeSocialMediaSchema(
                    youtube_id=request.social_media.youtube.youtube_id,
                    youtube_is_following=request.social_media.youtube.youtube_is_following,
                    youtube_is_viewed=request.social_media.youtube.youtube_is_viewed,
                    youtube_view_date=request.social_media.youtube.youtube_view_date,
                ),
                created_at=new_social_media.created_at,
                updated_at=new_social_media.updated_at,
                custom_logs=new_social_media.custom_logs,
            ),
        )

    if request.type == "facebook":
        new_social_media = SocialMediaModel(
            user_id=request.user_id,
            facebook_id=request.social_media.facebook.facebook_id,
            facebook_is_following=request.social_media.facebook.facebook_is_following,
            facebook_followed_date=request.social_media.facebook.facebook_followed_date,
            custom_logs=request.social_media.custom_logs,
        )
        db.add(new_social_media)
        db.commit()
        db.refresh(new_social_media)
        return SocialMediaCreateResponseSchema(
            user_id=new_social_media.user_id,
            social_media=SocialMediaBaseSchema(
                id=new_social_media.id,
                facebook=FacebookSocialMediaSchema(
                    facebook_id=request.social_media.facebook.facebook_id,
                    facebook_is_following=request.social_media.facebook.facebook_is_following,
                    facebook_followed_date=request.social_media.facebook.facebook_followed_date,
                ),
                created_at=new_social_media.created_at,
                updated_at=new_social_media.updated_at,
                custom_logs=new_social_media.custom_logs,
            ),
        )

    if request.type == "instagram":
        new_social_media = SocialMediaModel(
            user_id=request.user_id,
            instagram_id=request.social_media.instagram.instagram_id,
            instagram_is_following=request.social_media.instagram.instagram_is_following,
            instagram_follow_trigger_verify_date=request.social_media.instagram.instagram_follow_trigger_verify_date,
            instagram_followed_date=request.social_media.instagram.instagram_followed_date,
            instagram_tagged=request.social_media.instagram.instagram_tagged,
            instagram_tagged_date=request.social_media.instagram.instagram_tagged_date,
            instagram_reposted=request.social_media.instagram.instagram_reposted,
            instagram_reposted_date=request.social_media.instagram.instagram_reposted_date,
            custom_logs=request.social_media.custom_logs,
        )
        db.add(new_social_media)
        db.commit()
        db.refresh(new_social_media)
        return SocialMediaCreateResponseSchema(
            user_id=new_social_media.user_id,
            social_media=SocialMediaBaseSchema(
                id=new_social_media.id,
                instagram=InstagramSocialMediaSchema(
                    instagram_id=request.social_media.instagram.instagram_id,
                    instagram_is_following=request.social_media.instagram.instagram_is_following,
                    instagram_follow_trigger_verify_date=request.social_media.instagram.instagram_follow_trigger_verify_date,
                    instagram_followed_date=request.social_media.instagram.instagram_followed_date,
                    instagram_tagged=request.social_media.instagram.instagram_tagged,
                    instagram_tagged_date=request.social_media.instagram.instagram_tagged_date,
                    instagram_reposted=request.social_media.instagram.instagram_reposted,
                    instagram_reposted_date=request.social_media.instagram.instagram_reposted_date,
                ),
                created_at=new_social_media.created_at,
                updated_at=new_social_media.updated_at,
                custom_logs=new_social_media.custom_logs,
            ),
        )
    if request.type == "telegram":
        new_social_media = SocialMediaModel(
            user_id=request.user_id,
            telegram_id=request.social_media.telegram.telegram_id,
            telegram_is_following=request.social_media.telegram.telegram_is_following,
            telegram_followed_date=request.social_media.telegram.telegram_followed_date,
            custom_logs=request.social_media.custom_logs,
        )
        db.add(new_social_media)
        db.commit()
        db.refresh(new_social_media)
        return SocialMediaCreateResponseSchema(
            user_id=new_social_media.user_id,
            social_media=SocialMediaBaseSchema(
                id=new_social_media.id,
                instagram=InstagramSocialMediaSchema(
                    telegram_id=request.social_media.telegram.telegram_id,
                    telegram_is_following=request.social_media.telegram.telegram_is_following,
                    telegram_followed_date=request.social_media.telegram.telegram_followed_date,
                ),
                created_at=new_social_media.created_at,
                updated_at=new_social_media.updated_at,
                custom_logs=new_social_media.custom_logs,
            ),
        )
    if request.type == "x":
        new_social_media = SocialMediaModel(
            user_id=request.user_id,
            x_id=request.social_media.x.x_id,
            x_is_following=request.social_media.x.x_is_following,
            x_followed_date=request.social_media.x.x_followed_date,
            custom_logs=request.social_media.custom_logs,
        )
        db.add(new_social_media)
        db.commit()
        db.refresh(new_social_media)
        return SocialMediaCreateResponseSchema(
            user_id=new_social_media.user_id,
            social_media=SocialMediaBaseSchema(
                id=new_social_media.id,
                x=XSocialMediaSchema(
                    x_id=request.social_media.x.x_id,
                    x_is_following=request.social_media.x.x_is_following,
                    x_followed_date=request.social_media.x.x_followed_date,
                ),
                created_at=new_social_media.created_at,
                updated_at=new_social_media.updated_at,
                custom_logs=new_social_media.custom_logs,
            ),
        )

    if request.type == "discord":
        new_social_media = SocialMediaModel(
            user_id=request.user_id,
            discord_id=request.social_media.discord.discord_id,
            discord_is_following=request.social_media.discord.discord_is_following,
            discord_followed_date=request.social_media.discord.discord_followed_date,
            custom_logs=request.social_media.custom_logs,
        )
        db.add(new_social_media)
        db.commit()
        db.refresh(new_social_media)
        return SocialMediaCreateResponseSchema(
            user_id=new_social_media.user_id,
            social_media=SocialMediaBaseSchema(
                id=new_social_media.id,
                instagram=InstagramSocialMediaSchema(
                    discord_id=request.social_media.discord.discord_id,
                    discord_is_following=request.social_media.discord.discord_is_following,
                    discord_followed_date=request.social_media.discord.discord_followed_date,
                ),
                created_at=new_social_media.created_at,
                updated_at=new_social_media.updated_at,
                custom_logs=new_social_media.custom_logs,
            ),
        )



def retrieve_social_media(id: Optional[int], user_id: Optional[int], db: Session) -> SocialMediaRetrievalResponseSchema:
    if not id and not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing id or user_id")
    
    base_query = db.query(SocialMediaModel)
    filters = []
    
    if id is not None:
        filters.append(SocialMediaModel.id == id)
    
    if user_id is not None:
        filters.append(SocialMediaModel.user_id == user_id)
    
    if filters:
        existing_social_media = base_query.filter(*filters).first()
        
        if not existing_social_media:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Social media not found")
        try:
            return SocialMediaRetrievalResponseSchema(
                user_id=existing_social_media.user_id,
                social_media=SocialMediaBaseSchema(
                    id=existing_social_media.id,
                    youtube_id=existing_social_media.youtube_id,
                    youtube_is_following=existing_social_media.youtube_is_following,
                    youtube_is_viewed=existing_social_media.youtube_is_viewed,
                    youtube_view_date=existing_social_media.youtube_view_date,
                    facebook_id=existing_social_media.facebook_id,
                    facebook_is_following=existing_social_media.facebook_is_following,
                    facebook_followed_date=existing_social_media.facebook_followed_date,
                    instagram_id=existing_social_media.instagram_id,
                    instagram_is_following=existing_social_media.instagram_is_following,
                    instagram_follow_trigger_verify_date=existing_social_media.instagram_follow_trigger_verify_date,
                    instagram_followed_date=existing_social_media.instagram_followed_date,
                    instagram_tagged=existing_social_media.instagram_tagged,
                    instagram_tagged_date=existing_social_media.instagram_tagged_date,
                    instagram_reposted=existing_social_media.instagram_reposted,
                    instagram_reposted_date=existing_social_media.instagram_reposted_date,
                    telegram_id=existing_social_media.telegram_id,
                    telegram_is_following=existing_social_media.telegram_is_following,
                    telegram_followed_date=existing_social_media.telegram_followed_date,
                    x_id=existing_social_media.x_id,
                    x_is_following=existing_social_media.x_is_following,
                    x_followed_date=existing_social_media.x_followed_date,
                    discord_id=existing_social_media.discord_id,
                    discord_is_following=existing_social_media.discord_is_following,
                    discord_followed_date=existing_social_media.discord_followed_date,
                    custom_logs=existing_social_media.custom_logs,
                    updated_at=existing_social_media.updated_at,
                    created_at=existing_social_media.created_at,
                ),
            )
        except Exception as e:
            logging.error(f"An error occurred: {e}")

def retrieve_social_media_list(
    user_ids: List[int], db: Session
) -> List[SocialMediaRetrievalResponseSchema]:
    if not user_ids:
        raise HTTPException(status_code=400, detail="User IDs are required")
    else:
        existing_social_media = db.query(SocialMediaModel).filter(
            SocialMediaModel.user_id.in_(user_ids)
        )
        return [
            SocialMediaRetrievalResponseSchema(
                user_id=so.user_id,
                social_media=SocialMediaBaseSchema(
                    id=so.id,
                    youtube_id=so.youtube_id,
                    youtube_is_following=so.youtube_is_following,
                    youtube_is_viewed=so.youtube_is_viewed,
                    youtube_view_date=so.youtube_view_date,
                    facebook_id=so.facebook_id,
                    facebook_is_following=so.facebook_is_following,
                    facebook_followed_date=so.facebook_followed_date,
                    instagram_id=so.instagram_id,
                    instagram_is_following=so.instagram_is_following,
                    instagram_follow_trigger_verify_date=so.instagram_follow_trigger_verify_date,
                    instagram_followed_date=so.instagram_followed_date,
                    instagram_tagged=so.instagram_tagged,
                    instagram_tagged_date=so.instagram_tagged_date,
                    instagram_reposted=so.instagram_reposted,
                    instagram_reposted_date=so.instagram_reposted_date,
                    telegram_id=so.telegram_id,
                    telegram_is_following=so.telegram_is_following,
                    telegram_followed_date=so.telegram_followed_date,
                    x_id=so.x_id,
                    x_is_following=so.x_is_following,
                    x_followed_date=so.x_followed_date,
                    discord_id=so.discord_id,
                    discord_is_following=so.discord_is_following,
                    discord_followed_date=so.discord_followed_date,
                    custom_logs=so.custom_logs,
                    updated_at=so.updated_at,
                    created_at=so.created_at,
                ),
            )
            for so in existing_social_media
        ]


def update_social_media(
    request: SocialMediaUpdateRequestSchema, db: Session
) -> SocialMediaUpdateResponseSchema:
    if not request.id or not request.social_media or not request.type:
        raise HTTPException(status_code=400, detail="ID and Social media and type are required")
    existing_social_media = (
        db.query(SocialMediaModel).filter(SocialMediaModel.id == request.id).first()
    )
    if not existing_social_media:
        raise HTTPException(status_code=404, detail="Social media not found")
    if request.type == "youtube":
            if request.social_media.youtube:
                existing_social_media.youtube_id = request.social_media.youtube.youtube_id
                existing_social_media.youtube_is_following = request.social_media.youtube.youtube_is_following
                existing_social_media.youtube_is_viewed = request.social_media.youtube.youtube_is_viewed
                existing_social_media.youtube_view_date = request.social_media.youtube.youtube_view_date
                existing_social_media.custom_logs = request.social_media.custom_logs
                db.commit()
                db.refresh(existing_social_media)
                return SocialMediaUpdateResponseSchema(
                    user_id=existing_social_media.user_id,
                    social_media=SocialMediaCategrizedBaseScehma(
                        id=existing_social_media.id,
                        youtube=YoutubeSocialMediaSchema(
                            youtube_id=existing_social_media.youtube_id,
                            youtube_is_following=existing_social_media.youtube_is_following,
                            youtube_is_viewed=existing_social_media.youtube_is_viewed,
                            youtube_view_date=existing_social_media.youtube_view_date,
                        ),
                        created_at=existing_social_media.created_at,
                        updated_at=existing_social_media.updated_at,
                        custom_logs=existing_social_media.custom_logs,
                    ),
                )
    if request.type == "facebook":
            if request.social_media.facebook:
                existing_social_media.facebook_id = request.social_media.facebook.facebook_id
                existing_social_media.facebook_is_following = request.social_media.facebook.facebook_is_following
                existing_social_media.facebook_followed_date = request.social_media.facebook.facebook_followed_date
                existing_social_media.custom_logs = request.social_media.custom_logs

                db.commit()
                db.refresh(existing_social_media)
                return SocialMediaUpdateResponseSchema(
                    user_id=existing_social_media.user_id,
                    social_media=SocialMediaCategrizedBaseScehma(
                        id=existing_social_media.id,
                        facebook=FacebookSocialMediaSchema(
                            facebook_id=existing_social_media.facebook_id,
                            facebook_is_following=existing_social_media.facebook_is_following,
                            facebook_followed_date=existing_social_media.facebook_followed_date,
                        ),
                        created_at=existing_social_media.created_at,
                        updated_at=existing_social_media.updated_at,
                        custom_logs=existing_social_media.custom_logs,
                    ),
                )
    if request.type == "instagram":
            if request.social_media.instagram:
                existing_social_media.instagram_id = request.social_media.instagram.instagram_id
                existing_social_media.instagram_is_following = request.social_media.instagram.instagram_is_following
                existing_social_media.instagram_follow_trigger_verify_date = request.social_media.instagram.instagram_follow_trigger_verify_date
                existing_social_media.instagram_followed_date = request.social_media.instagram.instagram_followed_date
                existing_social_media.instagram_tagged = request.social_media.instagram.instagram_tagged
                existing_social_media.instagram_tagged_date = request.social_media.instagram.instagram_tagged_date
                existing_social_media.instagram_reposted = request.social_media.instagram.instagram_reposted
                existing_social_media.instagram_reposted_date = request.social_media.instagram.instagram_reposted_date
                existing_social_media.custom_logs = request.social_media.custom_logs
                db.commit()
                db.refresh(existing_social_media)
                return SocialMediaUpdateResponseSchema(
                    user_id=existing_social_media.user_id,
                    social_media=SocialMediaCategrizedBaseScehma(
                        id=existing_social_media.id,
                        instagram=InstagramSocialMediaSchema(
                            instagram_id=existing_social_media.instagram_id,
                            instagram_is_following=existing_social_media.instagram_is_following,
                            instagram_follow_trigger_verify_date=existing_social_media.instagram_follow_trigger_verify_date,
                            instagram_followed_date=existing_social_media.instagram_followed_date,
                            instagram_tagged=existing_social_media.instagram_tagged,
                            instagram_tagged_date=existing_social_media.instagram_tagged_date,
                            instagram_reposted=existing_social_media.instagram_reposted,
                            instagram_reposted_date=existing_social_media.instagram_reposted_date,
                        ),
                        created_at=existing_social_media.created_at,
                        updated_at=existing_social_media.updated_at,
                        custom_logs=existing_social_media.custom_logs,
                    ),
                )
    if request.type == "telegram":
            if request.social_media.telegram:
                existing_social_media.telegram_id = request.social_media.telegram.telegram_id
                existing_social_media.telegram_is_following = request.social_media.telegram.telegram_is_following
                existing_social_media.telegram_followed_date = request.social_media.telegram.telegram_followed_date
                existing_social_media.custom_logs = request.social_media.custom_logs

                db.commit()
                db.refresh(existing_social_media)
                return SocialMediaUpdateResponseSchema(
                    user_id=existing_social_media.user_id,
                    social_media=SocialMediaCategrizedBaseScehma(
                        id=existing_social_media.id,
                        instagram=InstagramSocialMediaSchema(
                            telegram_id=existing_social_media.telegram_id,
                            telegram_is_following=existing_social_media.telegram_is_following,
                            telegram_followed_date=existing_social_media.telegram_followed_date,
                        ),
                        created_at=existing_social_media.created_at,
                        updated_at=existing_social_media.updated_at,
                        custom_logs=existing_social_media.custom_logs,
                    ),
                )
    
    if request.type == "x":
            if request.social_media.x:
                existing_social_media.x_id = request.social_media.x.x_id
                existing_social_media.x_is_following = request.social_media.x.x_is_following
                existing_social_media.x_followed_date = request.social_media.x.x_followed_date
                existing_social_media.custom_logs = request.social_media.custom_logs
                db.commit()
                db.refresh(existing_social_media)
                return SocialMediaUpdateResponseSchema(
                    user_id=existing_social_media.user_id,
                    social_media=SocialMediaCategrizedBaseScehma(
                        id=existing_social_media.id,
                        x=XSocialMediaSchema(
                            x_id=existing_social_media.x_id,
                            x_is_following=existing_social_media.x_is_following,
                            x_followed_date=existing_social_media.x_followed_date,
                        ),
                        created_at=existing_social_media.created_at,
                        updated_at=existing_social_media.updated_at,
                        custom_logs=existing_social_media.custom_logs,
                    ),
                )
    if request.type == "discord":
            if request.social_media.discord:
                existing_social_media.discord_id = request.social_media.discord.discord_id
                existing_social_media.discord_is_following = request.social_media.discord.discord_is_following
                existing_social_media.discord_followed_date = request.social_media.discord.discord_followed_date
                existing_social_media.custom_logs = request.social_media.custom_logs

                db.commit()
                db.refresh(existing_social_media)
                return SocialMediaUpdateResponseSchema(
                    user_id=existing_social_media.user_id,
                    social_media=SocialMediaCategrizedBaseScehma(
                        id=existing_social_media.id,
                        instagram=InstagramSocialMediaSchema(
                            discord_id=existing_social_media.discord_id,
                            discord_is_following=existing_social_media.discord_is_following,
                            discord_followed_date=existing_social_media.discord_followed_date,
                        ),
                        created_at=existing_social_media.created_at,
                        updated_at=existing_social_media.updated_at,
                        custom_logs=existing_social_media.custom_logs,
                    ),
                )


def delete_social_media(id: int, db: Session):
    """Delete the social media"""
    db_social_media = (
        db.query(SocialMediaModel).filter(SocialMediaModel.id == id).first()
    )
    if db_social_media:
        db.delete(db_social_media)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Social Media {id} not found",
        )
