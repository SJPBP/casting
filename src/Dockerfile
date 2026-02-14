FROM ghcr.io/astral-sh/uv:python3.14-alpine3.23

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app

# Then copy the rest of your code
COPY . /app

# Disable development dependencies
ENV UV_NO_DEV=1

# Sync the project into a new environment, asserting the lockfile is up to date
RUN uv init .
RUN uv lock

RUN uv sync --locked

# Install required packages
RUN uv pip install flask beautifulsoup4 lxml requests pychromecast mysql-connector-python


# Expose and tell what port to use
ENV PORT=5000

EXPOSE 5000

CMD ["uv", "run", "-m", "webapp.app"]




