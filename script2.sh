#!/bin/bash

output_log="/home/redbee/Documentos/discover/LogScript"

siteIdList=($(cat listadoSites))

nuevo_valor_idsmediospago='"139"'
nuevo_valor_idsprotocolos='"7"'
directorio_raiz="/home/redbee/Documentos/redbee/infra/DEC2-crons/cron-scripts/cierres-lotes/conf-visa/"

# Listar los archivos .conf en el directorio sin búsqueda recursiva
listadoArchivos=$(find "$directorio_raiz" -maxdepth 1 -type f -name "*.conf" ! -name "*bak*")

# Define un patrón regex para buscar todos los SiteIDs
regex_siteIds=$(IFS="|"; echo "${siteIdList[*]}")

# Para controlar por pantalla el estado
cantidadTotalDeArchivos=$(echo "$listadoArchivos" | wc -l)
files_processed=0

# Inicializar archivos
echo "$listadoArchivos" > listadoArchivos
printf "" > archivosAModificar

fechaInicioRevision=$(date "+%d/%m/%Y %H:%M:%S")

# Filtrar los archivos que contienen al menos uno de los SiteIDs
archivoConSiteids=()
for archivo in $listadoArchivos; do
    echo -n -e "  Archivo revisado: $files_processed de $cantidadTotalDeArchivos\r"
    contieneSiteID=false
    for siteId in "${siteIdList[@]}"; do
        if grep -q "\"$siteId\" => {" "$archivo"; then
            contieneSiteID=true
            break
        fi
    done
    if [ "$contieneSiteID" = true ]; then
        # Verificar si el archivo ya ha sido procesado
        if [[ ! " ${archivos_procesados[@]} " =~ " $archivo " ]]; then
            archivos_procesados+=("$archivo")
            echo "$archivo" >> archivosAModificar
            archivoConSiteids+=("$archivo")
        fi
    fi
    ((files_processed++))
done

echo -e "\n"
echo "  Archivos revisados: $cantidadTotalDeArchivos"
echo "  Archivos a modificar: $(cat archivosAModificar | wc -l)"

fechaInicioModificaicon=$(date "+%d/%m/%Y %H:%M:%S")

# Procesar los archivos que contienen SiteIDs
for archivo in "${archivoConSiteids[@]}"; do
    for siteId in "${siteIdList[@]}"; do
        if grep -q "\"$siteId\" => {" "$archivo"; then
            # Usar sed para actualizar con los nuevos valores
            sed -i "/\"$siteId\" => {/{
                N
                s/\(idsmediospago => \[.*\)\]/\1, $nuevo_valor_idsmediospago\]/
                N
                s/\(idsprotocolos => \[.*\)\]/\1, $nuevo_valor_idsprotocolos\]/
            }" "$archivo"
            echo "Archivo modificado $archivo"
        fi
    done
done

fechaFinScript=$(date "+%d/%m/%Y %H:%M:%S")


echo "Fecha inicio revision de conf: $fechaInicioRevision"
echo "Fecha inicio modificacion de conf: $fechaInicioModificaicon"
echo "Fecha fin de script: $fechaFinScript"
echo -e "\nFinalizo el script"
