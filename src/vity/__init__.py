"""Vity - AI-powered terminal assistant"""

import importlib.metadata

try:
    __version__ = importlib.metadata.version("vity")
except importlib.metadata.PackageNotFoundError:
    # Fallback for development installations
    __version__ = "0.0.0+dev"

__author__ = "Kaleab Ayenew"
__email__ = "ai@enhance.care" 