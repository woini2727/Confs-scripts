# Confs-scripts

En este repo se agrupan diferentes scripts que son utilizados para modificar los archivos .conf

## Requerimientos
1. Tener instalado python 3.6+

## Script de actualización de configuración FTP2

### Inputs para pruebas

```sh
python3 update-ftp.py ./DEC2-crons "00200115,83008290,00130415" 0 1 "192.168.0.1" "new_userftp2" "new_passftp2" "new_remotefileftp2_%dd%mm%yy.%mediopago.txt"
```

Prueba los siguientes casos:
1. 00200115: Modifica la configuración FTP2 de un site que ya tenía configurado el FTP2. Este site tiene una pw con caracteres especiales, así que también testea que no fallen las REGEX.
2. 83008290: Agrega la configuración FTP2 de un site, que no es el primero ni el último en la lista de sites. Testea que agregue la coma luego de cerra la llave
3. 00130415: Agrega la configuración FTP2 del último site en la lista. Testea que **no** agregue la coma luego de cerrar la llave
4. FTP en 0 y SFTP en 1 (como lo usa centralpos)
5. Host con IP (como lo usa centralpos)

---

```sh
python3 update-ftp.py ./DEC2-crons "00200115" 1 0 "new.hostftp2.com" "new_userftp2" "n3w_pa#[]ºª|@~½¬¡{}ç+-\()&,.0" "lote87654321_%dd%mm%yy.%mediopago.txt"
```

Prueba los siguientes casos:
1. Actualizar 1 solo site a la vez
2. Una password con caracteres especiales.
3. Host con nombre de dominio
4. FTP en 1 y SFTP en 0 (insecure)

---

```sh
python3 update-ftp.py ./DEC2-crons "00200115" 1 0 "new.hostftp2.com" "new_userftp2" "\!n3w_pa\$\$#-\"()&,.'0" "lote87654321_%dd%mm%yy.%mediopago.txt"
```

#### IMPORANTE
Esta prueba falla por:
1. El caracter `!` se omite a pesar de ser escapado. Al menos así sucede en linux donde se probó.
2. El caracter `'` hace que se rompa el archivo .conf ya que es el mismo que se usa para delimitar los strings.
3. Los caracteres `$` y `"` necesitan ser escapados, como se muestra en el ejemplo (al menos en linux donde se probó). Si bien esto no hace que falle el script, se debe tener la precaución de escapar estos caracteres.

**Idealmente realizaría estas validaciones en el facade para que tire un bad request y que no lleguen al script**

---

```sh
python3 update-ftp.py ./DEC2-crons "00191130" 1 0 "new.hostftp2.com" "new_userftp2" "pass" "lote00191130_%dd%mm%yy.%mediopago.txt"
```

Prueba los siguientes casos:
1. Actualiza el site `00191130`, el cual está en 2 archivos al mismo tiempo. El programa debe actualizar la config en ambos sites y retornar en la respuesta los 2 archivos en los que se encontró el site