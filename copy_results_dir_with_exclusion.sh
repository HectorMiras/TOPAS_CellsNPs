#!/bin/bash

# === CONFIGURACIÓN ===
SOURCEDIR="/home/radiofisica/hector/mytopassimulations/TOPAS_CellsNPs/work/CellColony-med5-cell5"
TARGETDIR="/media/radiofisica/UBUNTU 22_0/only_results_CellColony-med5-cell5"

# Lista de exclusión: rutas relativas desde SOURCEDIR
EXCLUDE_LIST=(
  "**/supportFiles/"
  "**/*.sh"
  "**/Foci*.*"
  "**/I125Beam*.*"
  "**/nucleus_PHSP.phsp"
)

# === EJECUCIÓN ===

# Crear directorio de destino si no existe
mkdir -p "$TARGETDIR"

# Crear archivo temporal con exclusiones
EXCLUDE_FILE=$(mktemp)
for item in "${EXCLUDE_LIST[@]}"; do
  echo "$item" >> "$EXCLUDE_FILE"
done

# Ejecutar copia con rsync usando exclusiones
rsync -av --exclude-from="$EXCLUDE_FILE" "$SOURCEDIR/" "$TARGETDIR/"

# Eliminar archivo temporal
rm "$EXCLUDE_FILE"

