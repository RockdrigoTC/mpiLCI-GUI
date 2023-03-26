# mpiLCI-GUI

### mpiLCI-GUI es una herramienta para compilar y ejecutar programas MPI en un servidor Linux. Con mpiLCI, puedes compilar y ejecutar programas MPI de manera sencilla y rápida.

## Dependencias
### Servidor
  - mpi
  - ssh-server
  
### Cliente
- ssh-client
- python
- Paramiko
   ``` sh
   pip install paramiko
   ```
   
## Instalación
### -Servidor

#### Clonar el repositorio y colocar los directorios
``` sh
clone https://github.com/RockdrigoTC/mpiLCI-GUI.git
cd mpiLCI-GUI
mkdir ~/MPI
cp -r sourceMPI buildMPI machinefileMPI outputMPI ~/
```
#### Colocar los scripts en una ruta accesible para la terminal por ejemplo: ``` /usr/bin/ ```
``` sh
cp mpiLCIFunctions /usr/bin/mpiLCIFunctions
```
#### Otorgarle los permisos de ejecucion al script
``` sh
sudo chmod +x /usr/bin/mpiLCIFunctions
```
### -Cliente

#### Asegurarse de tener todos los requisitos previos para realizar una conexion ssh con el servidor
#### Ejecutar mpiLCI.py en el cliente
