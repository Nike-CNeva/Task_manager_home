{ pkgs, ... }:

let
  my-python = pkgs.python311.withPackages (ps: with ps; [
    # Основные
    fastapi
    uvicorn
    sqlalchemy
    pydantic
    alembic
    python-dotenv
    psycopg2
    passlib

    # Дополнительные зависимости из requirements.txt
    pydantic-settings
    pydantic-extra-types
    email-validator
    python-multipart
    orjson
    ujson
    click
    jinja2
    markupsafe
    rich
    pygments
    typing-extensions
    cryptography
    cffi
    pycparser
    websockets
    python-jose
    # Возможно пригодятся:
    itsdangerous
  ]);
in
{
  channel = "stable-24.05";

  packages = [
    my-python
  ];

  idx.previews = {
      enable = true;
      previews = {
        web = {
          command = [
          "npm"
          "run"
          "start"
          "--"
          "--port"
          "$PORT"
          "--host"
          "0.0.0.0"
          "--disable-host-check"];
          manager = "web";
          env = {
            PORT = "$PORT";
          };

        };
        backend = {
          command = ["uvicorn" "main:app" "--host" "0.0.0.0" "--port" "$PORT"];
          manager = "web";
          env = {
            PORT = "$PORT";
          };

        };
      };
    };

}
