import numpy as np
from tqdm import tqdm
import time
import rasterio
from gbofe_tools import get_neighbors, get_slopes, get_factor

def request_paths():
    """
    Asks the user for the necessary file paths and the gradient value.

    Returns:
        tuple or None: (ruta_dem, ruta_drenajes, gradiente, ruta_salida, method) if the
        values are valid, otherwise None.
    """
    path_dem = input('Enter the path of the Digital Elevation Model (DEM): ')
    path_drainage = input('Enter the path of the accumulated flow drainage raster: ')
    method = int(input('1: r.carve\n' +
                       '2: Normal Excavation\n' +
                       '3: Normal Excavation Modified\n' +
                       '4: Gradient-Based Optimized Flow Enforcement (GBOFE)\n\n' +
                       'Choose the flow-enforcement method: '))

    try:
        gradient = float(input('Enter the gradient descent value (G) {G > 0}: '))
        if gradient <= 0:
            raise ValueError
    except ValueError:
        print("Please enter a positive numerical value for the gradient.")
        return None

    path_out = input('Enter the output path for the corrected DEM: ')

    return path_dem, path_drainage, gradient, path_out, method


def correct_dem(path_dem_, path_drainage_, gradient_, path_out_, method_):
    if method_ == 4:
        with rasterio.open(path_dem_) as base:
            base_transform = base.transform
            base_width = base.width
            base_height = base.height
            base_crs = base.crs
            # Se asume que los píxeles son cuadrados, por lo que la resolución se extrae de 'a'
            res = abs(base_transform.a)
            # Extraer el array del raster base
            base_array = base.read(1).astype(np.float64)
            nodata = base.nodata

            # Reemplazar valores NoData por NaN
            if nodata is not None:
                base_array = np.where(base_array == nodata, np.nan, base_array)
            # Crea un copia del dem
            dem_burnstream = np.copy(base_array)

        with rasterio.open(path_drainage_) as drainage:
            band_drainage = drainage.read(1).astype(np.int32)
            # Crea una copia del drenaje
            array_drainage = np.copy(band_drainage)

        # Parametro mínimo de flujo
        flow_accum = 1
        values_fa = array_drainage.ravel()
        values_flow_accum = values_fa[values_fa >= flow_accum]
        set_values = np.unique(values_flow_accum)

        # Iterar sobre cada valor de flujo seleccionado
        for i in tqdm(range(len(set_values))):
            node = set_values[i]
            indices = np.argwhere(array_drainage == node)

            for z in range(len(indices)):
                idx = indices[z]
                # Obtener vecinos
                alt_vecinos = get_neighbors(dem_burnstream, idx)
                fa_vecinos = get_neighbors(array_drainage, idx)

                altura = dem_burnstream[idx[0], idx[1]]

                if max(fa_vecinos[:, 0]) != 0:
                    # Calcular pendientes
                    pendientes_vecinos = get_slopes(alt_vecinos[:, 0], altura, res)

                    # Añadir las pendientes a la matriz alt_vecinos
                    alt_vecinos = np.concatenate((alt_vecinos, pendientes_vecinos), axis=1)

                    # Luego añadir los valores de fa_vecinos
                    # Se forma una matriz con: elevación, fila, columna, pendiente y flujo acumulado
                    fa_vecinos_col = fa_vecinos[:, 0].reshape(-1, 1)
                    alt_vecinos = np.concatenate((alt_vecinos, fa_vecinos_col), axis=1)

                    # Eliminar la fila donde fa == node
                    alt_vecinos = alt_vecinos[alt_vecinos[:, 4] != node]

                    # valores mayores que node
                    col5 = alt_vecinos[:, 4]
                    superiores = col5[col5 > node]

                    if superiores.size > 0:
                        minimo_sup = superiores.min()
                        # quedarnos con filas cuyo col3 <= node o cuyo col3 == mínimo_sup
                        alt_vecinos = alt_vecinos[(col5 <= node) | (col5 == minimo_sup)]

                    # Encontrar los vecinos con mayor valor de FA (flujo acumulado)
                    max_fa = np.max(alt_vecinos[:, 4]) # 3053
                    ind_mod = np.argwhere(alt_vecinos[:, 4] == max_fa) # 3

                    # Verificar si existe una pendiente positiva
                    max_pend = np.max(alt_vecinos[:, 3]) # 0.003118

                    if not (max_pend > 0):
                        # Si no hay pendiente positiva, se iguala la altura del vecino con mayor FA
                        dem_burnstream[
                            alt_vecinos[ind_mod, 1].astype(int),
                            alt_vecinos[ind_mod, 2].astype(int)
                        ] = altura
                        array_drainage[idx[0], idx[1]] = 0
                    else:
                        # Si existe pendiente positiva
                        ind_pend = np.argwhere(alt_vecinos[:, 3] == max_pend) # 0

                        # Caso 1: Si solo hay un vecino con FA máximo
                        if len(ind_mod) == 1:
                            # Si el vecino de FA máximo no coincide con el max_pend o hay múltiples pendientes máximas
                            if (alt_vecinos[ind_mod[0, 0], 3] != max_pend) or (len(ind_pend) > 1):
                                slope = max_pend + gradient_
                                factor = get_factor(ind_mod[0, 0], res)
                                dem_burnstream[
                                    int(alt_vecinos[ind_mod[0, 0], 1]),
                                    int(alt_vecinos[ind_mod[0, 0], 2])
                                ] = altura - slope * factor
                                array_drainage[idx[0], idx[1]] = 0

                        else:
                            # Caso 2: Hay múltiples vecinos con FA máximo
                            # Verificar si alguno de ellos tiene la pendiente máxima
                            pendientes_fa_max = alt_vecinos[ind_mod[:, 0], 3]
                            tiene_max_pend = np.any(np.isin(pendientes_fa_max, alt_vecinos[ind_pend, 3]))

                            # Si ninguno de los vecinos con FA máx. tiene pendiente máx. o si
                            # el número de vecinos con FA máximo es menor que el número con pendiente máx.
                            # entonces se corrige la altura de todos esos vecinos de FA máx.
                            if (not tiene_max_pend) or (len(ind_mod) < len(ind_pend)):
                                slope = max_pend + gradient_
                                for idx_mod in ind_mod:
                                    vecino_ind = idx_mod[0]
                                    factor = get_factor(vecino_ind, res)
                                    dem_burnstream[
                                        int(alt_vecinos[vecino_ind, 1]),
                                        int(alt_vecinos[vecino_ind, 2])
                                    ] = altura - slope * factor
                                    array_drainage[idx[0], idx[1]] = 0
                else:
                    array_drainage[idx[0], idx[1]] = 0

        # Guardar el raster corregido
        with rasterio.open(
            path_out_, "w",
            driver="GTiff",
            height=base_height,
            width=base_width,
            count=1,
            dtype=rasterio.float64,
            crs=base_crs,
            transform=base_transform,
            nodata=nodata
        ) as dst:
            dst.write(dem_burnstream, 1)

if __name__ == "__main__":
    parameters = request_paths()
    if parameters:
        start_time = time.time()
        correct_dem(*parameters)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Tiempo de ejecución: {execution_time} segundos")