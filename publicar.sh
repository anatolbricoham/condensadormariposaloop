#!/bin/sh
# Publica este repositorio en GitHub.
# Uso:  sh publicar.sh https://github.com/TU_USUARIO/condensador-mariposa-loop.git
# Antes crea el repositorio VACÍO en https://github.com/new (sin README ni licencia).
set -e
[ -z "$1" ] && { echo "Uso: sh publicar.sh URL_DEL_REPOSITORIO"; exit 1; }
cd "$(dirname "$0")"
git remote remove origin 2>/dev/null || true
git remote add origin "$1"
git push -u origin main
git push origin --tags
echo "Publicado en $1"
