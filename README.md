# Airflow MinIO PostgreSQL Pipeline

Apache Airflow 3 ilə MinIO və PostgreSQL inteqrasiyasını nümayiş etdirən sadə pipeline layihəsi.

## Layihə nə edir?

- `minio_bash_task` DAG-ı `BashOperator` və MinIO Client (`mc`) istifadə edərək `bronze.py` faylını MinIO-ya yükləyir və yoxlayır.
- `postgres_hook_task` DAG-ı `PostgresHook` vasitəsilə PostgreSQL bağlantısını test edir.
- Bütün servislər Docker Compose ilə birlikdə işə salınır.

## Texnologiyalar

- Apache Airflow 3.1.0
- PostgreSQL 16
- MinIO Community Edition
- Docker Compose
- Python

## İşə salınma

1. `.env` faylı yaradın və PostgreSQL, Airflow və MinIO dəyişənlərini əlavə edin.
2. Servisləri başladın:

```bash
docker compose up -d --build
```

3. Airflow interfeysini açın:

```text
http://localhost:8081
```

4. MinIO Console-a keçin:

```text
http://localhost:9003
```

5. Airflow UI-da aşağıdakı DAG-ları aktivləşdirib başladın:

- `minio_bash_task`
- `postgres_hook_task`

## Portlar

| Servis | Host portu |
|---|---:|
| Airflow API | 8081 |
| PostgreSQL | 5436 |
| MinIO API | 9002 |
| MinIO Console | 9003 |

> Qeyd: Airflow Connection bölməsində `postgres_exam` adlı PostgreSQL connection yaradılmalıdır. MinIO DAG-ının işləməsi üçün `matrix` bucket-i və uyğun MinIO credentials da konfiqurasiya edilməlidir.
