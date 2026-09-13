from enum import Enum

from pydantic import BaseModel

from traka_automation.util.config import secrets_config


class EmailSettings(BaseModel):
    mailbox: str
    signature_name: str
    signature_title: str


class MollieSettings(BaseModel):
    api_key: str


class PayNlSettings(BaseModel):
    service_id: str
    secret: str


class MsGraphSettings(BaseModel):
    tenant_id: str
    client_id: str
    client_secret: str


class PaymentServiceProvider(Enum):
    MOLLIE = "mollie"
    PAYNL = "paynl"


class AppSettings(BaseModel):
    dev: bool
    payment_service_provider: PaymentServiceProvider
    email: EmailSettings
    ms_graph: MsGraphSettings
    mollie: MollieSettings | None = None
    paynl: PayNlSettings | None = None


def get_settings() -> AppSettings:
    config = secrets_config
    payment_service_provider = PaymentServiceProvider(
        config["payment_service_provider"]
    )
    settings_data = {
        "dev": config["dev"],
        "payment_service_provider": payment_service_provider,
        "email": config["email"],
        "ms_graph": config["ms_graph"],
    }
    if payment_service_provider == PaymentServiceProvider.MOLLIE:
        settings_data["mollie"] = config["mollie"]
    if payment_service_provider == PaymentServiceProvider.PAYNL:
        settings_data["paynl"] = config["paynl"]
    return AppSettings.model_validate(settings_data)
