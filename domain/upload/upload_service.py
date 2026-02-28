from fastapi import UploadFile
from domain.upload.crypto import derive_key_and_seed, encrypt_bytes
from datetime import datetime, timezone
import hmac
import hashlib
import uuid
import json
import os
from dotenv import load_dotenv

ENV = os.getenv("ENV", "development")

load_dotenv(f".env.{ENV}")


async def handle_upload(file: UploadFile, password: str) -> str:
    unique_id = str(uuid.uuid4())

    enc_key, seed = derive_key_and_seed(password, unique_id)

    plaintext: bytes = await file.read()

    print(len(plaintext))

    encrypted_blob: bytes = encrypt_bytes(
        enc_key=enc_key,
        plaintext=plaintext,
    )

    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))

    shards = split_into_shards(encrypted_blob, CHUNK_SIZE)

    for index, shard in enumerate(shards):
        store_shard(
            shard=shard,
            seed=seed,
            index=index,
        )

    store_metadata(unique_id=unique_id, num_shards=len(shards), chunk_size=CHUNK_SIZE)

    return unique_id


def store_metadata(
    unique_id: str,
    num_shards: int,
    chunk_size: int,
) -> None:
    metadata = {
        "unique_id": unique_id,
        "num_shards": num_shards,
        "chunk_size": chunk_size,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    os.makedirs("metadata", exist_ok=True)

    path = os.path.join("metadata", f"{unique_id}.json")

    with open(path, "w") as f:
        json.dump(metadata, f)

    return


def split_into_shards(data: bytes, chunk_size: int) -> list[bytes]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")

    return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]


def store_shard(shard: bytes, seed: bytes, index: int):
    index_bytes = index.to_bytes(4, "big")

    path_hash = hmac.new(seed, index_bytes, hashlib.sha256).hexdigest()

    dir1 = path_hash[:2]
    dir2 = path_hash[2:4]

    path = os.path.join("storage", dir1, dir2, path_hash)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "wb") as f:
        f.write(shard)

    return
