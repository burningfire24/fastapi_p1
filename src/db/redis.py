import asyncio
from redis import redis

from .config import config

token_blocklist = Redis(
    host=config.HOST,
    port=config.PORT,
    db=0
)

JTI_EXPIRY = config.REFRESH_TOKEN_EXPIRE_DAYS

async def add_jti_to_blocklist(jti: str, expires_in: int = JTI_EXPIRY ) -> None:
    await token_blocklist.set(
        name=f"blocklist:{jti}",
        value="revoked",
        ex=expires_in,
    )

async def token_in_blocklist(jti: str) -> bool:
    return await token_blocklist.exists(f"blocklist:{jti}") == 1

asyncio.run(main())

