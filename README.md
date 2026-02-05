## 사용자 요구사항

1. **저장 서버는 업로드된 파일을 원본 형태로 저장해서는 안 되며,  
   서버가 보유한 정보만으로는 파일을 복구할 수 없어야 한다.**

2. **업로드된 파일은 단일 객체가 아닌 분할된 형태로 저장되어야 하며,  
   제3자가 이를 하나의 파일 구조로 파악할 수 없어야 한다.**

3. **파일의 저장 위치 및 재구성 방식은 사용자 비밀번호를 기반으로 결정되어야 하며,  
   업로드 시 사용된 비밀번호 없이는 파일을 복원할 수 없어야 한다.**

---

## 핵심 컴포넌트 (Core Components)

### 1. 비밀번호 기반 경로 유도

- 파일은 저장될 때 하나의 위치에 저장되지 않고,  
  **업로드 시 사용된 비밀번호를 기준으로 계산된 경로들**에 조각 단위로 분산 저장된다.
- 서버는 파일 조각의 위치 정보를 별도로 저장하지 않으며,  
  동일한 비밀번호가 제공될 때만 파일을 다시 구성할 수 있다.
- 이로 인해 서버나 제3자는 파일 조각 간의 관계를 알 수 없다.

---

### 2. 파일 조각 분산 저장

- 업로드된 파일은 여러 개의 조각으로 나뉘어 저장된다.
- 각 조각은 전역적으로 공유되는 스토리지 공간에 섞여 저장되며,  
  파일 시스템 상에서는 하나의 파일로 인식되지 않는다.
- 이를 통해 파일의 구조나 경계를 외부에서 파악하기 어렵게 한다.

---

### 3. Merkle Tree 기반 무결성 검증

- 저장된 파일 조각을 기반으로 무결성 정보를 생성하여 파일 변조 여부를 검증한다.
- 파일을 다시 조립할 때 조각 단위로 검증이 가능하며,  
  손상된 조각을 빠르게 식별할 수 있다.
- 필요 시 손상된 조각만을 선택적으로 복구할 수 있도록 설계되었다.

## 기술 스택 (Technology Stack)

- **Backend Framework**
  - FastAPI
  - Uvicorn

- **Cryptography & Identifier Libraries**
  - cryptography
  - hashlib
  - uuid

## 암호화 알고리즘 (Cryptographic Algorithms)

- **Unique Identifier**
  - UUIDv4

- **Hash Algorithm**
  - SHA-256

- **Symmetric Encryption**
  - AES-256-GCM

- **Key Derivation**
  - PBKDF2-HMAC-SHA256

- **Integrity Verification**
  - Merkle Tree (SHA-256)

## 사용자 사용 흐름 (User Flow)

- **Upload Flow**
![upload-flow](https://private-user-images.githubusercontent.com/77044696/545517500-04279899-b07e-4478-b8d9-9008b4451864.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzAyODcxMTgsIm5iZiI6MTc3MDI4NjgxOCwicGF0aCI6Ii83NzA0NDY5Ni81NDU1MTc1MDAtMDQyNzk4OTktYjA3ZS00NDc4LWI4ZDktOTAwOGI0NDUxODY0LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAyMDUlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMjA1VDEwMjAxOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTRlYTFmNWJmNzQ5MjRjY2NhMGViOGIzNGI4Yzg4OGE4YzEzMGE2ZTMzYWI4YmFlNWUxZDVlMTU2MjA3YjgxNWYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.XWZp230XxWaihv_3Wxmn9yfo3IoomGIyO2xLyMnLhDU)

---

- **Download Flow**
![download-flow](https://private-user-images.githubusercontent.com/77044696/545515122-a74b77db-d958-45ab-a35b-05f47749d12d.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzAyODY4ODQsIm5iZiI6MTc3MDI4NjU4NCwicGF0aCI6Ii83NzA0NDY5Ni81NDU1MTUxMjItYTc0Yjc3ZGItZDk1OC00NWFiLWEzNWItMDVmNDc3NDlkMTJkLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAyMDUlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMjA1VDEwMTYyNFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTE5OWU2MDhkNmY3NmM3YTVmNGQzMGVhNzY5MWRjYWE3NjY3YjljNTg0MDFjZDNlODZlNWYxMDVkYmY3YjM3MDkmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.FDa0xF7227jigcAr1K8KGhfQ-hhQx3XIgYfSafXBcTY)