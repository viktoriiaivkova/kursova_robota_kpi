from pydantic import BaseModel, EmailStr, ConfigDict

class UserBaseDTO(BaseModel):
    username: str
    email: EmailStr
class UserCreateDTO(UserBaseDTO):
    pass
class UserResponseDTO(UserBaseDTO):
    id: int
    model_config = ConfigDict(from_attributes=True)
class AccountBaseDTO(BaseModel):
    acc_name: str
    balance: float = 0.0
    user_id: int
class AccountCreateDTO(AccountBaseDTO):
    pass
class AccountResponseDTO(AccountBaseDTO):
    id: int
    model_config = ConfigDict(from_attributes=True)