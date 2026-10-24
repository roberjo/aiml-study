"""One LLM client for the whole repo, free providers only.

Every provider here speaks the OpenAI-compatible API, so a single SDK covers all of them.
Switch with environment variables (in .env):

    LLM_PROVIDER=gemini   # free tier, strong model (default); needs GEMINI_API_KEY
    LLM_PROVIDER=groq     # free tier, very fast open models; needs GROQ_API_KEY
    LLM_MODEL=...         # optional override of the provider's default model
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDERS = {
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "key_env": "GEMINI_API_KEY",
        "model": "gemini-2.5-flash",
        "embed_model": "gemini-embedding-001",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "key_env": "GROQ_API_KEY",
        "model": "openai/gpt-oss-120b",
        "embed_model": None,
    },
}


def _config(provider: str | None) -> tuple[str, dict]:
    name = provider or os.getenv("LLM_PROVIDER", "gemini")
    if name not in PROVIDERS:
        raise ValueError(f"Unknown LLM_PROVIDER {name!r}; choose from {list(PROVIDERS)}")
    return name, PROVIDERS[name]


def client(provider: str | None = None) -> tuple[OpenAI, str]:
    """Return an OpenAI-compatible client and the model name to use with it."""
    name, cfg = _config(provider)
    key = os.getenv(cfg["key_env"])
    if not key:
        raise RuntimeError(f"Set {cfg['key_env']} in .env to use {name}")
    model = os.getenv("LLM_MODEL", cfg["model"])
    return OpenAI(base_url=cfg["base_url"], api_key=key), model


def chat(prompt: str, system: str | None = None, provider: str | None = None, **kwargs) -> str:
    """Single-turn completion. Pass temperature, max_tokens, etc. through kwargs.

    Reasoning models (gpt-oss, Gemini 2.5) spend tokens thinking before they answer: a small
    max_tokens can return an empty string. Leave it unset or give it a few hundred.
    """
    llm, model = client(provider)
    messages = [{"role": "system", "content": system}] if system else []
    messages.append({"role": "user", "content": prompt})
    response = llm.chat.completions.create(model=model, messages=messages, **kwargs)
    return response.choices[0].message.content


def embed(texts: list[str], provider: str | None = None) -> list[list[float]]:
    """Embed a batch of texts. Groq has no embeddings endpoint, so it falls back to Gemini."""
    name, cfg = _config(provider)
    if cfg["embed_model"] is None:
        name, cfg = _config("gemini")
    llm, _ = client(name)
    response = llm.embeddings.create(model=cfg["embed_model"], input=texts)
    return [item.embedding for item in response.data]
