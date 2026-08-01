from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def generate_enrollment_email(name: str, camp: str, payment_link: str, cost: float) -> str:
    """Generate an enrollment email_handler in HTML."""
    env = Environment(
        loader=FileSystemLoader(Path(__file__).resolve().parent.parent / "templates"),
        autoescape=True,
    )

    template = env.get_template("enrollment_confirmation.html")
    html = template.render(
        participant_names=name,
        camp_name=camp,
        payment_url=payment_link,
        amount=cost,
        signature_name="Wouter van Harten",
        signature_title="Penningmeester Plusscoutskring Trapperskamp",
        logo_url="https://next.trapperskamp.com/processed_images/trapperskamp-vught.a83be22bfa0f671b.webp",
    )

    return html