# mpiLCI-GUI

### mpiLCI-GUI es una herramienta para compilar y ejecutar programas MPI en un servidor Linux. Con mpiLCI, puedes compilar y ejecutar programas MPI de manera sencilla y rápida.

## Dependencias
### Servidor
  - [mpi](https://www.mpich.org/)
  - ssh-server
  
### Cliente
- ssh-client
- [Python](https://www.python.org/downloads/)
- [pip](https://pypi.org/project/pip/)
- [Paramiko](https://pypi.org/project/paramiko/)
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
cp -r sourceMPI buildMPI machinefileMPI outputMPI ~/MPI/
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

#### Asegurarse de tener todos los requisitos previos para realizar una conexión ssh con el servidor
#### Ejecutar mpiLCI.py en el cliente
