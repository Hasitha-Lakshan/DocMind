FROM postgres:17

# Install dependencies
RUN apt update && apt install -y git build-essential postgresql-server-dev-17 \
    && git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make \
    && make install \
    && rm -rf /var/lib/apt/lists/*

# Ensure PostgreSQL starts correctly
CMD ["postgres"]
