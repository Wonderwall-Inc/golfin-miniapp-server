# from app.user.schemas import (
#     UserAppInfoSchema,
#     UserPersonalInfoSchema,
#     UserTelegramInfoSchema,
#     UserCreateRequestSchema,
#     UserCreateResponseSchema,
#     UserRetrivalRequestSchema,
#     UserRetrivalResponseSchema,
#     UserUpdateRequestSchema,
#     UserUpdateResponseSchema,
#     UserUpdateDetailsSchema,
#     UserDetailsSchema,
#     UserSchema,
#     UserDetailsResponseSchema,
# )

# from app.game_character.schemas import (
#     GameCharacterBaseSchema,
#     GameCharacterStatBaseSchema,
#     GameCharacterStatsSchema,
#     GameCharacterSchema,
#     GameCharacterDetailsSchema,
#     GameCharacterStatDetailsSchema,
#     GameCharacterCreateDetailsSchema,
#     GameCharacterCreateRequestSchema,
#     GameCharacterCreateResponseSchema,
#     GameCharacterUpdateDetailsSchema,
#     GameCharacterStatsUpdateDetailsSchema,
#     GameCharacterRetrivalRequestSchema,
#     GameCharacterRetrivalResponseSchema,
#     GameCharacterStatRetrivalRequestSchema,
#     GameCharacterStatRetrivalResponseSchema,
#     GameCharacterUpdateRequestSchema,
#     GameCharacterUpdateResponseSchema,
# )


# class UserSchemaFactory:
#     """User Factory for creating schema objects"""

#     def __init__(
#         self,
#         payload: (
#             UserCreateRequestSchema
#             | UserSchema
#             | UserDetailsSchema
#             | UserUpdateDetailsSchema
#         ),
#     ):
#         self.payload = payload

#     def userAppInfoSchemaMaker(self) -> UserAppInfoSchema:
#         return UserAppInfoSchema(
#             is_active=self.payload.app_info.is_active,
#             in_game_items=self.payload.app_info.in_game_items,
#             is_admin=self.payload.app_info.is_admin,
#             skin=self.payload.app_info.skin,
#         )

#     def userPersonalInfoSchemaMaker(self) -> UserPersonalInfoSchema:
#         return UserAppInfoSchema(
#             location=self.payload.personal_info.location,
#             nationality=self.payload.personal_info.nationality,
#             age=self.payload.personal_info.age,
#             gender=self.payload.personal_info.gender,
#             email=self.payload.personal_info.email,
#         )

#     def userTelegramInfoSchemaMaker(self) -> UserTelegramInfoSchema:
#         return UserTelegramInfoSchema(
#             username=self.payload.telegram_info.username,
#             telegram_id=self.payload.telegram_info.telegram_id,
#             token_balance=self.payload.telegram_info.token_balance,
#             is_premium=self.payload.telegram_info.is_premium,
#             wallet_address=self.payload.telegram_info.wallet_address,
#             chat_id=self.payload.telegram_info.chat_id,
#         )

#     def userSchemaMaker(self) -> UserSchema:
#         return UserSchema(
#             id=self.payload.id,
#             app_info=self.userAppInfoSchemaMaker(),
#             personal_info=self.userPersonalInfoSchemaMaker(),
#             telegram_info=self.userTelegramInfoSchemaMaker(),
#             created_at=self.payload.created_at,
#             updated_at=self.payload.updated_at,
#             custom_logs=self.payload.custom_logs,
#         )

#     def userCreateResponseSchemaMaker(self) -> UserCreateResponseSchema:
#         return UserCreateResponseSchema(
#             access_token=self.payload.access_token,
#             user_details=UserDetailsSchema(user_base=self.userSchemaMaker()),
#         )

#     def userDetailsResponseSchemaMaker(self) -> UserDetailsResponseSchema:
#         return UserDetailsSchema(
#             user_base=self.userSchemaMaker(),
#             game_characters=self.payload.game_characters,
#             point=self.payload.point,
#             activity=self.payload.activity,
#             social_media=self.payload.social_media,
#             sender=self.payload.sender,
#             reciver=self.payload.receiver,
#         )

#     def userUpdateResponseSchemaMaker(self) -> UserUpdateResponseSchema:
#         return UserUpdateResponseSchema(
#             user_details=self.userDetailsResponseSchemaMaker()
#         )

#     # def userUpdateDetailsSchemaMaker(self) -> UserUpdateDetailsSchema:
#     #     return UserUpdateDetailsSchema(
#     #         token_balance=self.payload.token_balance,
#     #         is_active=self.payload.is_active,
#     #         is_premium=self.payload.is_premium,
#     #         in_game_items=self.payload.in_game_items,
#     #         skin=self.payload.skin,
#     #         location=self.payload.location,
#     #         age=self.payload.age,
#     #         custom_logs=self.payload.custom_logs,
#     #     )


# class GameCharacterSchemaFactory:
#     """Game Character Factory for creating schema objects"""

#     def __init__(
#         self,
#         payload: (
#             GameCharacterBaseSchema
#             | GameCharacterStatBaseSchema
#             | GameCharacterStatsSchema
#             | GameCharacterSchema
#             | GameCharacterDetailsSchema
#             | GameCharacterStatDetailsSchema
#             | GameCharacterCreateDetailsSchema
#             | GameCharacterUpdateDetailsSchema
#             | GameCharacterStatsUpdateDetailsSchema
#             | GameCharacterCreateRequestSchema
#             | GameCharacterCreateResponseSchema
#             | GameCharacterRetrivalRequestSchema
#             | GameCharacterStatRetrivalRequestSchema
#             | GameCharacterStatRetrivalResponseSchema
#             | GameCharacterUpdateRequestSchema
#             | GameCharacterUpdateResponseSchema
#         ),
#     ):
#         self.payload = payload

#     def gameCharacterBaseSchema(self) -> GameCharacterBaseSchema:
#         return GameCharacterBaseSchema(
#             id=self.payload.id,
#             first_name=self.payload.first_name,
#             last_name=self.payload.last_name,
#             gender=self.payload.gender,
#             created_at=self.payload.created_at,
#             updated_at=self.payload.updated_at,
#             custom_logs=self.payload.custom_logs,
#         )

#     def gameCharacterStatBaseSchema(self) -> GameCharacterStatBaseSchema:
#         return GameCharacterStatBaseSchema(
#             id=self.payload.id,
#             level=self.payload.level,
#             exp_points=self.payload.exp_points,
#             stamina=self.payload.stamina,
#             recovery=self.payload.recovery,
#             condition=self.payload.condition,
#         )

#     def gameCharacterStatsSchema(self) -> GameCharacterStatsSchema:
#         return GameCharacterStatsSchema(
#             id=self.payload.id,
#             level=self.payload.level,
#             exp_points=self.payload.exp_points,
#             stamina=self.payload.stamina,
#             recovery=self.payload.recovery,
#             condition=self.payload.condition,
#             created_at=self.payload.created_at,
#             updated_at=self.payload.updated_at,
#         )

#     def gameCharacterSchema(self) -> GameCharacterSchema:
#         return GameCharacterSchema(
#             id=self.payload.id,
#             first_name=self.payload.first_name,
#             last_name=self.payload.last_name,
#             gender=self.payload.gender,
#             title=self.payload.title,
#             created_at=self.payload.created_at,
#             updated_at=self.payload.updated_at,
#             custom_logs=self.payload.custom_logs,
#         )

#     def gameCharacterDetailsSchema(self) -> GameCharacterDetailsSchema:
#         return GameCharacterDetailsSchema(
#             game_character_base=self.gameCharacterSchema(), user_id=self.payload.user_id
#         )

#     def gameCharacterStatDetailsSchema(self) -> GameCharacterStatDetailsSchema:
#         return GameCharacterStatDetailsSchema(
#             game_character_stat_base=self.gameCharacterStatsSchema(),
#             game_character_id=self.payload.game_character_id,
#         )

#     def gameCharacterCreateDetailsSchema(self) -> GameCharacterCreateDetailsSchema:
#         return GameCharacterCreateDetailsSchema(
#             first_name=self.payload.first_name,
#             last_name=self.payload.last_name,
#             gender=self.payload.gender,
#             title=self.payload.title,
#             custom_logs=self.payload.custom_logs,
#         )

#     def gameCharacterUpdateDetailsSchema(self) -> GameCharacterUpdateDetailsSchema:
#         return GameCharacterUpdateDetailsSchema(
#             first_name=self.payload.first_name,
#             last_name=self.payload.last_name,
#             gender=self.payload.gender,
#             title=self.payload.title,
#             custom_logs=self.payload.custom_logs,
#         )

#     def gameCharacterStatsUpdateDetailsSchema(
#         self,
#     ) -> GameCharacterStatsUpdateDetailsSchema:
#         return GameCharacterStatsUpdateDetailsSchema(
#             level=self.payload.level,
#             exp_points=self.payload.exp_points,
#             stamina=self.payload.stamina,
#             recovery=self.payload.recovery,
#             condition=self.payload.condition,
#             custom_logs=self.payload.custom_logs,
#         )

#     def gameCharacterCreateRequestSchema(self) -> GameCharacterCreateRequestSchema:
#         return GameCharacterCreateRequestSchema(
#             user_id=self.payload.user_id,
#             access_token=self.payload.access_token,
#             character_details=self.gameCharacterCreateDetailsSchema(),
#         )

#     def gameCharacterCreateResponseSchema(self) -> GameCharacterCreateResponseSchema:
#         return GameCharacterCreateResponseSchema(
#             game_character_id=self.payload.game_character_id,
#             character_stats=self.gameCharacterStatDetailsSchema(),
#         )

#     def gameCharacterRetrivalRequestSchema(self) -> GameCharacterRetrivalRequestSchema:
#         return GameCharacterRetrivalRequestSchema(
#             access_token=self.payload.access_token,
#             id=self.payload.id,
#             character_details=self.gameCharacterDetailsSchema(),
#         )

#     def GameCharacterRetrivalResponseSchema(
#         self,
#     ) -> GameCharacterRetrivalResponseSchema:
#         return GameCharacterRetrivalResponseSchema(
#             character_details=self.gameCharacterDetailsSchema(),
#             character_stats=self.gameCharacterStatDetailsSchema(),
#         )

#     def gameCharacterStatRetrivalRequestSchema(
#         self,
#     ) -> GameCharacterStatRetrivalRequestSchema:
#         return GameCharacterStatRetrivalRequestSchema(
#             access_token=self.payload.access_token,
#             id=self.payload.id,
#             character_stats=self.gameCharacterStatDetailsSchema(),
#         )

#     def gameCharacterStatRetrivalResponseSchema(
#         self,
#     ) -> GameCharacterStatRetrivalRequestSchema:
#         character_stats: GameCharacterStatDetailsSchema
#         return GameCharacterStatRetrivalRequestSchema(character_stats=character_stats)

#     def gameCharacterUpdateRequestSchema(self) -> GameCharacterUpdateRequestSchema:
#         return GameCharacterUpdateRequestSchema(
#             user_id=self.payload.user_id,
#             access_token=self.payload.access_token,
#             game_character_id=self.payload.game_character_id,
#             character_details=self.gameCharacterDetailsSchema(),
#             character_stats=self.gameCharacterStatsSchema(),
#         )

#     def gameCharacterUpdateResponseSchema(self) -> GameCharacterUpdateResponseSchema:
#         return GameCharacterUpdateRequestSchema(
#             character_details=self.gameCharacterDetailsSchema(),
#             character_stats=self.gameCharacterStatsSchema(),
#         )
