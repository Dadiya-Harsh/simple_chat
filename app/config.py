from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import logging
from pathlib import Path

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    
    app_name: str =  Field(description="My Application name")
    debug_level: str = Field(description="Debug level for the application", default="INFO")
    deployment_port: int = Field(description="Port for deployment")
    mcp_hosted_port: int = Field(description="Port for MCP hosted service")
    
    openai_api_key: str = Field(description="OpenAI API Key")
    
    groq_api_key: str = Field(description="Groq API Key")
    
    gemini_api_key: str = Field(description="Gemini API Key")
    
settings = AppSettings()

def get_logger(module_name: str) -> logging.Logger:
    """Get a configured logger for the specified module.
    
    Sets both console and file handlers with the debug level from settings.
    
    Args:
        module_name (str): The name of the module for which the logger is created.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(module_name)
    logger.setLevel(settings.debug_level)

    # Avoid adding handlers multiple times (common pitfall)
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # ---- Console Handler ----
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.debug_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # ---- File Handler ----
    log_filename = f"{module_name.replace('.', '_')}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(settings.debug_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger