#!/usr/bin/env python3

import os
import re
import json



def update_existing_ftp2(new_ftp2_config, site_content):
    """
    Pisa la configuración FTP2 existente con la que se le pasa por parámetro

    :return: el objeto site con la configuración FTP2 actualizada.
    """

    updated_site_content = re.sub(
        r'(ftp2\s*=>\s*)\d+,',
        f'ftp2 => {new_ftp2_config["ftp2"]},',
        site_content
    )
    updated_site_content = re.sub(
        r'(sftp2\s*=>\s*)\d+,',
        f'sftp2 => {new_ftp2_config["sftp2"]},',
        updated_site_content
    )
    updated_site_content = re.sub(
        r'(hostftp2\s*=>\s*)\'[^\']+\',',
        f'hostftp2 => \'{new_ftp2_config["hostftp2"]}\',',
        updated_site_content
    )
    updated_site_content = re.sub(
        r'(userftp2\s*=>\s*)\'[^\']+\',',
        f'userftp2 => \'{new_ftp2_config["userftp2"]}\',',
        updated_site_content
    )
    updated_site_content = re.sub(
        r'(passftp2\s*=>\s*)\'[^\']+\',',
        f'passftp2 => \'{new_ftp2_config["passftp2"]}\',',
        updated_site_content
    )

    # TODO: Acá con la coma tengo que aplicar la misma lógica que hago en el método de agregar
    # OJO: acá hay que pensar si conviene dejarla como está o actualizarla
    #   - Ventaja de actualizar: puedo permitir que se guarde en un subdirectorio FTP que sugiera instore (que hoy no es un requisito)
    #   - Desventaja de actualizar: tengo que implementar la lógica para hacer en eso en el facade
    # updated_site_content = re.sub(
    #     r'(remotefileftp2\s*=>\s*)\'[^\']+\',',
    #     f'remotefileftp2 => \'{new_ftp2_config["remotefileftp2"]}\',', # FIXME: Esta coma no está de más? Sip. Ver el primer site de prueba
    #     updated_site_content
    # )

    return updated_site_content



def add_ftp2(new_ftp2_config, site_content, site_id):
    """
    Recibe un objeto site sin los campos de FTP2 y le concatena al final del objeto la configuración recibida por parámetro.
    
    :return: el objeto site con la configuración FTP2 agregada.
    """

    ftp2_config_str = (
        f'\t\tftp2 => {new_ftp2_config["ftp2"]},\n'
        f'\t\tsftp2 => {new_ftp2_config["sftp2"]},\n'
        f'\t\thostftp2 => \'{new_ftp2_config["hostftp2"]}\',\n'
        f'\t\tuserftp2 => \'{new_ftp2_config["userftp2"]}\',\n'
        f'\t\tpassftp2 => \'{new_ftp2_config["passftp2"]}\',\n'
        f'\t\tremotefileftp2 => \'lote{site_id}_%dd%mm%yy.%mediopago.txt\'\n'
    )

    # La f al inicio es para interpolar la REGEX con la variable `ftp2_config_str`
    replacement = f',\n{ftp2_config_str}'+'}\n'

    # Agrega: una coma, el salto de linea, la config ftp2 y por ultimo, la llave de cierre
    # Además, si después de la llave de cierre tenía una coma, entonces agrego la coma al final.
    # Es necesario evaluar esto porque, el último objeto de la lista de sites, no lleva la coma al final
    if re.search(r'(\s*},)$', site_content):
        replacement = f',\n{ftp2_config_str}'+'},'

    # Busca la ultima llave `}` para insertar la nueva configuración FTP2 antes del cierre de la sección del site
    # Es necesario agregar la llave al final xq `re.sub()` reemplaza lo que encontró (la llave) con lo que le paso.
    updated_site_content = re.sub(r'(\s*}[\s*|,]*)$', replacement, site_content)

    return updated_site_content



def update_ftp2_config(directory, site_ids, new_ftp2_config):
    """
    Recorre todos los archivos .conf en un directorio y subdirectorios, buscando múltiples sites específicos
    y actualiza o agrega la configuración FTP2. Retorna un diccionario con los sites actualizados y sus archivos.

    :param directory: Directorio base donde buscar los archivos .conf
    :param site_ids: Lista de IDs de los sites que se buscan
    :param new_ftp2_config: Diccionario con la nueva configuración FTP2
    :return: Diccionario con los sites actualizados y los archivos donde se encontraron
    """

    # Variable en la que voy escribiendo la respuesta. Es un JSON.
    updated_sites = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.conf'):
                file_path = os.path.join(root, file)

                with open(file_path, 'r') as f:
                    content = f.read()

                
                for site_id in site_ids:
                    # Expresión regular para encontrar la sección del site en el archivo .conf
                    # Esta expresión regular fallaba cuando hay un corchete en un lugar inesperado, por ej passftp
                    # Por eso tuve que poner como condición que luego del corchete tenga una coma y line break o solo line break
                    # El flag re.DOTALL hace el que el punto "." matchee también el caracter de newline
                    site_pattern = re.compile(rf'("{site_id}"\s*=>\s*{{.*?}}[,\n|\s*?\n])', re.DOTALL)
                    match = site_pattern.search(content)
                    
                    if match:
                        site_content = match.group(1)

                        if 'ftp2' in site_content:
                            updated_site_content = update_existing_ftp2(new_ftp2_config, site_content)
                        else:
                            updated_site_content = add_ftp2(new_ftp2_config, site_content, site_id)

                        # Reemplazo en el string que contiene todo el archivo, SOLO el site que acabo de editar
                        content = content.replace(site_content, updated_site_content)

                        with open(file_path, 'w') as f:
                            f.write(content)

                        if site_id not in updated_sites:
                            updated_sites.append(site_id)
                        
                f.close()

    return updated_sites



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Actualizar configuración FTP2 en archivos .conf")
    parser.add_argument("directory", help="Directorio base donde buscar los archivos .conf")
    parser.add_argument("site_ids", help="Lista de IDs de los sites que se buscan (separados por comas)")
    parser.add_argument("ftp2", type=int, help="Valor de FTP2")
    parser.add_argument("sftp2", type=int, help="Valor de SFTP2")
    parser.add_argument("hostftp2", help="Host FTP2")
    parser.add_argument("userftp2", help="Usuario FTP2")
    parser.add_argument("passftp2", help="Contraseña FTP2")
    #parser.add_argument("remotefileftp2", help="Archivo remoto FTP2. Es un template")

    args = parser.parse_args()

    site_ids = args.site_ids.split(',')

    new_ftp2_config = {
        "ftp2": args.ftp2,
        "sftp2": args.sftp2,
        "hostftp2": args.hostftp2,
        "userftp2": args.userftp2,
        "passftp2": args.passftp2,
        #"remotefileftp2": args.remotefileftp2
    }

    updated_sites = update_ftp2_config(args.directory, site_ids, new_ftp2_config)

    print(updated_sites)
