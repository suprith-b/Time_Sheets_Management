from app.core.exceptions import InvalidInputDataError
import re

class InputValidation:

    @staticmethod
    def validate_length( field: str, data: str, length: int ) -> None:
        if len( data ) > length:
            raise InvalidInputDataError( f"{field} is too long. Max - {length} characters" )

    @staticmethod
    def validate_phone_number(phone_number: str) -> None:
        if len( phone_number ) != 10 or ( not phone_number.isdigit() ) :
            raise InvalidInputDataError("invalid phone number")

    @staticmethod  
    def validate_email( email: str ) -> None:
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        match = re.fullmatch(pattern, email)
        if match is None or not match:
            raise InvalidInputDataError( "invalid email address" )
