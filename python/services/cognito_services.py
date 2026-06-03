import boto3
import os
from utils.logger import get_logger

from utils.exceptions import (
    UserAlreadyExistsError,
    InvalidPasswordError,
    InvalidRequestError,
    InvalidCredentialsError
)

client = boto3.client("cognito-idp")
logger = get_logger(__name__)

CLIENT_ID = os.environ["CLIENT_ID"]


def register_user(email, password):
    try:
        return client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[{"Name": "email", "Value": email}]
        )
    
    except client.exceptions.UsernameExistsException:
        raise UserAlreadyExistsError()
    except client.exceptions.InvalidPasswordException:
        raise InvalidPasswordError()
    except Exception as e:
        raise InvalidRequestError(str(e))


def verify_otp(email, otp):
    try:
        return client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            ConfirmationCode=otp
        )
    except client.exceptions.CodeMismatchException:
        raise InvalidRequestError("Invalid OTP code")
    except client.exceptions.ExpiredCodeException:
        raise InvalidRequestError("OTP has expired. Please request a new one")
    except Exception as e:
        raise InvalidRequestError(str(e))


def login_user(email, password):
    try:
        return client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            ClientId=CLIENT_ID,
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password
            }
        )
    except client.exceptions.NotAuthorizedException:
        raise InvalidCredentialsError()
    except client.exceptions.UserNotConfirmedException:
        raise InvalidRequestError("Email not verified. Please verify OTP first")
    except Exception as e:
        raise InvalidRequestError(str(e))