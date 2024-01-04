PAV - P4: reconocimiento y verificación del locutor
===================================================

Obtenga su copia del repositorio de la práctica accediendo a [Práctica 4](https://github.com/albino-pav/P4)
y pulsando sobre el botón `Fork` situado en la esquina superior derecha. A continuación, siga las
instrucciones de la [Práctica 2](https://github.com/albino-pav/P2) para crear una rama con el apellido de
los integrantes del grupo de prácticas, dar de alta al resto de integrantes como colaboradores del proyecto
y crear la copias locales del repositorio.

También debe descomprimir, en el directorio `PAV/P4`, el fichero [db_8mu.tgz](https://atenea.upc.edu/mod/resource/view.php?id=3654387?forcedownload=1)
con la base de datos oral que se utilizará en la parte experimental de la práctica.

Como entrega deberá realizar un *pull request* con el contenido de su copia del repositorio. Recuerde
que los ficheros entregados deberán estar en condiciones de ser ejecutados con sólo ejecutar:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.sh
  make release
  run_spkid mfcc train test classerr verify verifyerr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recuerde que, además de los trabajos indicados en esta parte básica, también deberá realizar un proyecto
de ampliación, del cual deberá subir una memoria explicativa a Atenea y los ficheros correspondientes al
repositorio de la práctica.

A modo de memoria de la parte básica, complete, en este mismo documento y usando el formato *markdown*, los
ejercicios indicados.

## Ejercicios.

### SPTK, Sox y los scripts de extracción de características.

- Analice el script `wav2lp.sh` y explique la misión de los distintos comandos involucrados en el *pipeline*
  principal (`sox`, `$X2X`, `$FRAME`, `$WINDOW` y `$LPC`). Explique el significado de cada una de las 
  opciones empleadas y de sus valores.

  1. `sox`
      - `$inputfile`: Nombre del archivo de audio de entrada en formato WAV.
      - `-t raw -e signed -b 16`: Establece el formato de salida a datos de audio en crudo con codificación de 16 bits
  2. `$X2X`
      - `$X2X +sf`: Convierte los datos de entrada en formato binario a números en formato decimal.
  3. `$FRAME`
      - `-l 240 -p 80`: Divide la señal de entrada en frames de longitud 240 con un desplazamiento de 80 muestras entre cada frame. Esto se utiliza para segmentar la señal en fragmentos más pequeños para el análisis LPC.
  4. `$WINDOW`
      - `-l 240 -L 240`: Aplica a una ventana de longitud 240 a cada frame de la señal. Se usa para reducir errores en el dominio de la frecuencia.
  5. `$LPC`
      - `-l 240 -m $lpc_order`: Realiza el cálculo de los coeficientes LPC utilizando una longitud de análisis de 240 y un orden (`$lpc_oder`) que se pasa como argumento. Los coeficientes LPC se utilizan para modelar la resonancia del tracto vocal en segmentos de la señal.

- Explique el procedimiento seguido para obtener un fichero de formato *fmatrix* a partir de los ficheros de
  salida de SPTK (líneas 45 a 51 del script `wav2lp.sh`).

    1. Procesamiento de la señal de audio: 

      - Se utiliza `sox` para leer los archivos de entrada `$inputfile` y convertirlo a un formato de datos sin procesar (`-t raw`) con codificación de muestras de 16 bits (`-e signed -b 16`).
    2. Análisis LPC:

      - `$X2X +sf` convierte los datos de formato de binario a decimal. 
      - `$FRAME -l 240 -p 80` divide la señal en frames de longitud 240 con un desplazamiento de 80 muestras entre frames.
      - `$WINDOW -l 240 -L 240` aplica una ventana a cada frame.
      - `$LPC -l 240 -m $lpc_order` calcula los coeficientes LPC de orden `$lpc_order`para cada frame.
    3. Generación del archivo 'fmatrix`:

      - Se establece el número de columnas (`ncol`) como el orden LPC más uno (`lpc_order + 1`), ya que los coeficientes LPC incluyen el coeficiente de ganancia.
      - Se cuenta el número de filas (`nrow`) al dividir el número total de elementos en los archivos generados por el análisis LPC por el número de columnas.
      - Se crea un archivo de formato `fmatrix`comenzando en la escritura de `nrow`y `ncol` usando `$X2X +aI`.
      - Los coeficientes LPC calculados previamente de concatenan en el archivo `fmatrix` con el comando `cat`.


  * ¿Por qué es más conveniente el formato *fmatrix* que el SPTK?

    - Legibilidad y portabilidad: Los archivos `fmatrix` son legibles y pueden ser usados en varios programas debido a su formato de texto plano.
    - Interoperabilidad: No estan limitados a una herramienta específica.
    - Facilidad de manipulación: Son fáciles de manipular con scripts y programas. Permiten realizar diferentes operaciones sobre los datos.

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales de predicción lineal
  (LPCC) en su fichero <code>scripts/wav2lpcc.sh</code>: 

  sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 |
	$LPC -l 240 -m $lpc_order | $LPCC -m $lpc_order -M $lpcc_order > $base.lpcc || exit 1


- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales en escala Mel (MFCC) en su
  fichero <code>scripts/wav2mfcc.sh</code>:

  sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 | 
	$MFCC -l 240 -L 512 -w 0 -s 8.0 -n $mfcc_filter -m $mfcc_order > $base.mfcc || exit 1 

### Extracción de características.

- Inserte una imagen mostrando la dependencia entre los coeficientes 2 y 3 de las tres parametrizaciones
  para todas las señales de un locutor.
  
  + Indique **todas** las órdenes necesarias para obtener las gráficas a partir de las señales 
    parametrizadas.
  + ¿Cuál de ellas le parece que contiene más información?

- Usando el programa <code>pearson</code>, obtenga los coeficientes de correlación normalizada entre los
  parámetros 2 y 3 para un locutor, y rellene la tabla siguiente con los valores obtenidos.

  |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  | &rho;<sub>x</sub>[2,3] |      |      |      |
  
  + Compare los resultados de <code>pearson</code> con los obtenidos gráficamente.
  
- Según la teoría, ¿qué parámetros considera adecuados para el cálculo de los coeficientes LPCC y MFCC?

  La longitud de la ventana, el desplazamiento de la ventana, la elección de la ventana, el número de coeficientes a calcular y el número de filtros mel (en caso de los MFCC).Adjunte

### Entrenamiento y visualización de los GMM.

Complete el código necesario para entrenar modelos GMM.

- Inserte una gráfica que muestre la función de densidad de probabilidad modelada por el GMM de un locutor
  para sus dos primeros coeficientes de MFCC.

- Inserte una gráfica que permita comparar los modelos y poblaciones de dos locutores distintos (la gŕafica
  de la página 20 del enunciado puede servirle de referencia del resultado deseado). Analice la capacidad
  del modelado GMM para diferenciar las señales de uno y otro.

### Reconocimiento del locutor.

Complete el código necesario para realizar reconociminto del locutor y optimice sus parámetros.

- Inserte una tabla con la tasa de error obtenida en el reconocimiento de los locutores de la base de datos
  SPEECON usando su mejor sistema de reconocimiento para los parámetros LP, LPCC y MFCC.

### Verificación del locutor.

Complete el código necesario para realizar verificación del locutor y optimice sus parámetros.

- Inserte una tabla con el *score* obtenido con su mejor sistema de verificación del locutor en la tarea
  de verificación de SPEECON. La tabla debe incluir el umbral óptimo, el número de falsas alarmas y de
  pérdidas, y el score obtenido usando la parametrización que mejor resultado le hubiera dado en la tarea
  de reconocimiento.
  
  1. MFCC

![Alt text](https://github.com/xmasdeup/P4/Masdeu-Alsina/mfcc-errors.png?raw=true)  
![Alt text](https://github.com/xmasdeup/P4/Masdeu-Alsina/mfcc-cost.png?raw=true)

  2. LPCC

![Alt text](https://github.com/xmasdeup/P4/Masdeu-Alsina/lpcc-errors.png?raw=true)

![Alt text](https://github.com/xmasdeup/P4/Masdeu-Alsina/lpcc-cost.png?raw=true)
 
### Test final

- Adjunte, en el repositorio de la práctica, los ficheros `class_test.log` y `verif_test.log` 
  correspondientes a la evaluación *ciega* final.

### Trabajo de ampliación.

- Recuerde enviar a Atenea un fichero en formato zip o tgz con la memoria (en formato PDF) con el trabajo 
  realizado como ampliación, así como los ficheros `class_ampl.log` y/o `verif_ampl.log`, obtenidos como 
  resultado del mismo.
