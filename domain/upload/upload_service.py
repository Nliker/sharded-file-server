import uuid
from fastapi import UploadFile

from domain.upload.crypto import derive_key_and_seed, encrypt_bytes

N_SHARDS = 16


async def handle_upload(file: UploadFile, password: str) -> str:
    unique_id = str(uuid.uuid4())

    enc_key, seed = derive_key_and_seed(password, unique_id)

    print(enc_key.hex())
    print(seed.hex())

    plaintext: bytes = await file.read()

    encrypted_blob: bytes = encrypt_bytes(
        enc_key=enc_key,
        plaintext=plaintext,
    )

    shards = split_into_shards(encrypted_blob, N_SHARDS)

    for index, shard in enumerate(shards, start=1):
        store_shard(
            shard=shard,
            unique_id=unique_id,
            index=index,
        )

    return unique_id


def split_into_shards(data: bytes, n: int) -> list[bytes]:
    size = len(data)
    base = size // n
    rem = size % n

    shards = []
    offset = 0
    for i in range(n):
        chunk = base + (1 if i < rem else 0)
        shards.append(data[offset : offset + chunk])
        offset += chunk
    return shards


def store_shard(*, shard: bytes, unique_id: str, index: int):
    print(f"[STORE] uid={unique_id} part={index} size={len(shard)}")
